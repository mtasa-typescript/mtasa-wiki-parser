import enum
import os
import re
from typing import List, Dict, Any, Optional

import requests
from bs4 import BeautifulSoup

from fetch.function import FunctionUrl, FunctionType, FunctionArgument, FunctionData, CompoundFunctionData, \
    FunctionDoc, FunctionOOP
from fetch.globals import HOST_URL


# All this code looks like piece of ...
# Needs heavy refactoring into classes

class ParseFunctionType(enum.Enum):
    CLIENT = 'Client'
    SERVER = 'Server'
    SHARED = 'Shared'


def cut_start_by_regex(data: str, regex) -> [str, Any]:
    regex_result = re.search(regex, data)
    if not regex_result:
        return ['', None]

    return [data[regex_result.start():], regex_result]


# TODO: encapsulate into a class
def parse_get_function_description(data: str) -> str:
    description = ''
    for line in data.split('\n'):
        if line == '':
            continue

        if line.startswith(('{', '_')):
            continue

        if line.startswith('='):
            break  # Stop at first header

        description += f'{line}\n'

    return description[:-1]  # Remove last \n


def parse_get_function_code(data: str) -> str:
    SELECT_CODE_REGEX = re.compile(r'<syntaxhighlight[^>]*>([\s\S]+?)</syntaxhighlight>')
    return re.search(SELECT_CODE_REGEX, data).group(1)


def parse_get_function_signature(code: str) -> FunctionType:
    WORD_REGEX_END = re.compile(r'([a-zA-Z0-9.]+)$')
    WORD_REGEX = re.compile(r'([a-zA-Z0-9_]+)')

    bracket_start = code.index('(')
    before_bracket = code[:bracket_start].strip()
    after_bracket = code[bracket_start + 1:].strip()

    name_regex = re.search(WORD_REGEX_END, before_bracket)  # last word before the opening bracket is function name
    function_name = name_regex.group(1)

    return_types_str = before_bracket[:name_regex.start()]
    return_types = [t.strip() for t in return_types_str.split(' ') if t.strip() != '']
    return_types = [t.replace(',', '') for t in return_types]

    args: List[FunctionArgument] = []
    optional_arg = False
    for arg_signature in after_bracket.split(','):
        if arg_signature == ')':
            break  # No args

        if '...' in arg_signature:
            args.append(FunctionArgument(name='...args',
                                         argument_type='any[]',
                                         default_value=None,
                                         optional=True))
            continue

        # TODO: Looks like pipe-filter pattern. Refactoring?
        arg_signature = arg_signature.strip()
        arg_type_regex = re.search(WORD_REGEX, arg_signature)
        arg_type = arg_type_regex.group(1)

        arg_signature = arg_signature[arg_type_regex.end():].strip()
        arg_name_regex = re.search(WORD_REGEX, arg_signature)
        arg_name = arg_name_regex.group(1)

        arg_signature = arg_signature[arg_name_regex.end():].strip()
        arg_default = None
        if arg_signature.startswith('='):
            end_of_string_cut = re.search(r'[])]', arg_signature)  # end of string cutoff
            if end_of_string_cut:
                arg_signature = arg_signature[1:end_of_string_cut.start()]
            else:
                arg_signature = arg_signature[1:]

            arg_default = arg_signature.strip()

        args.append(FunctionArgument(name=arg_name,
                                     argument_type=arg_type,
                                     default_value=arg_default,
                                     optional=optional_arg))

        if '[' in arg_signature:
            optional_arg = True

    return FunctionType(name=function_name,
                        return_types=return_types,
                        arguments=args)


def parse_get_function_arguments_docs(data: str) -> Dict[str, str]:
    START_REGEX = re.compile(r'=+[A-Za-z0-9 ]*Arguments=+', re.IGNORECASE)
    data = cut_start_by_regex(data, START_REGEX)[0]

    docs: Dict[str, str] = dict()
    name = None
    for line in data.split('\n'):
        if line == '':
            continue

        if line.strip().startswith('='):
            if 'argument' not in line.lower():
                break
            else:
                continue

        name_regex = re.search(r"\* *'+([^':]+):?'+", line)
        if name_regex is None and name is not None:
            docs[name] += line + '\n'
            continue
        elif name_regex is None and name is None:
            print('[ERROR] Required Arguments wrong line')
            continue
        name = name_regex.group(1)

        line = line[name_regex.end():].strip()
        line = re.sub(r'[\[\]\'\"]', '', line)

        docs[name] = line + '\n'

    return {k: docs[k][:-1] for k in docs}  # remove \n


def parse_get_function_returns_doc(data: str) -> str:
    START_REGEX = re.compile(r'=Returns?=+', re.IGNORECASE)
    data = cut_start_by_regex(data, START_REGEX)[0]

    result = ''
    for line in data.split('\n'):
        if line == '':
            continue

        if line.strip().startswith('='):
            if 'return' not in line.lower():
                break
            else:
                continue

        result += line + '\n'

    return result[:-1]  # remove last line-break


def parse_get_function_type(data: str) -> ParseFunctionType:
    for line in data.split('\n'):
        line = line.strip().lower()
        if not line.startswith('{{'):
            continue

        if not 'function' in line:
            continue

        line = line[:re.search(r'}}', line).start()]  # Cut comments

        if re.search(r'(server[_ ]client|shared)[_ ]function', line, re.IGNORECASE):
            return ParseFunctionType.SHARED
        if 'client function' in line or 'client_function' in line:
            return ParseFunctionType.CLIENT
        if 'server function' in line or 'server_function' in line:
            return ParseFunctionType.SERVER

    raise RuntimeError('Cannot find function type')


def parse_get_function_oop(data: str) -> Optional[FunctionOOP]:
    MATCHER = re.compile(r'{{ *OOP *\|[^\|]*?\| *\[\[([^]]+)\]\] *[.:] *([^|]+)\|([^\|]*)')

    oop_result = re.search(MATCHER, data)
    if oop_result is None:
        return None

    class_name = oop_result.group(1)
    class_name = class_name.split('|')[-1]
    return FunctionOOP(class_name=class_name,
                       method_name=oop_result.group(2),
                       field=oop_result.group(3) if oop_result.group(3) else None)


def parse_apply_branches_and_bounds(data: str) -> str:
    END_CUTOFF_REGEX = re.compile(r'=+ *(See Also|Examples?) *=+', re.IGNORECASE)
    regexp_result = re.search(END_CUTOFF_REGEX, data)
    if regexp_result:
        data = data[:regexp_result.start()]  # Cutoff

    return data


def parse_two_sections(content: str, f_url: FunctionUrl) -> CompoundFunctionData:
    SERVER_SECTION = re.compile(r'<section.+class="server".*?>([\s\S]+?)<\/section>', re.IGNORECASE)
    CLIENT_SECTION = re.compile(r'<section.+class="client".*?>([\s\S]+?)<\/section>', re.IGNORECASE)

    description = parse_get_function_description(content)
    returns = parse_get_function_returns_doc(content)

    server_content = re.search(SERVER_SECTION, content).group(1)
    client_content = re.search(CLIENT_SECTION, content).group(1)
    result = CompoundFunctionData(server=parse_one_side_function(server_content, f_url),
                                  client=parse_one_side_function(client_content, f_url))

    result.client.docs.description = description
    result.server.docs.description = description

    if not result.client.docs.result:
        result.client.docs.result = returns
    if not result.server.docs.result:
        result.server.docs.result = returns

    return result


# only client or only server side
def parse_shared_side_function(content: str, f_url: FunctionUrl) -> CompoundFunctionData:
    if '<section' in content.lower():
        return parse_two_sections(content, f_url)

    # There are no sections
    all_data = parse_one_side_function(content, f_url)
    return CompoundFunctionData(server=all_data,
                                client=all_data)


def parse_one_side_function(content: str, f_url: FunctionUrl) -> FunctionData:
    content_code = parse_get_function_code(content)
    data = FunctionData(signature=parse_get_function_signature(content_code),
                        docs=FunctionDoc(description=parse_get_function_description(content),
                                         arguments=parse_get_function_arguments_docs(content),
                                         result=parse_get_function_returns_doc(content)),
                        url=f_url,
                        oop=parse_get_function_oop(content))
    if data.oop is None:
        print('[WARN] No OOP definition for', f_url.name)
    print('[INFO] Complete')

    return data


def parse(content: str, f_url: FunctionUrl, skip_shared: bool = False) -> Optional[CompoundFunctionData]:
    print('[INFO] Reading ', f_url.name)

    content = parse_apply_branches_and_bounds(content)  # Cutoff examples, see also

    type_of_function = parse_get_function_type(content)
    if type_of_function == ParseFunctionType.SHARED:
        if skip_shared:
            print(f'[INFO] Shared function {f_url.name} will be skipped')
            return None
        return parse_shared_side_function(content, f_url)

    data = parse_one_side_function(content, f_url)
    if type_of_function == ParseFunctionType.CLIENT:
        return CompoundFunctionData(client=data)

    if type_of_function == ParseFunctionType.SERVER:
        return CompoundFunctionData(server=data)


def get_function_data(f_url: FunctionUrl,
                      skip_shared: bool = False,
                      use_cache: bool = True) -> Optional[CompoundFunctionData]:
    name = f_url.name[0].upper() + f_url.name[1:]
    cache_file = os.path.join('dump-html', name)
    if os.path.exists(cache_file) and use_cache:
        with open(cache_file,'r', encoding='UTF-8') as cache:
            media_wiki = cache.read()
    else:
        url = f'{HOST_URL}/index.php?title={name}&action=edit'
        req = requests.request('GET', url)
        html = req.text
        soup_wiki = BeautifulSoup(html, 'html.parser')
        source_field = soup_wiki.select_one('#wpTextbox1')
        media_wiki = source_field.contents[0]

        with open(cache_file,'w', encoding='UTF-8') as cache:
            cache.write(media_wiki)

    return parse(media_wiki, f_url, skip_shared)
