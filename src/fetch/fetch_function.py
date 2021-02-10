import enum
import re
from typing import List, Dict

import requests
from bs4 import BeautifulSoup

from src.fetch.function import FunctionUrl, FunctionType, FunctionArgument
from src.fetch.globals import HOST_URL


class ParseFunctionType(enum.Enum):
    CLIENT = 'Client'
    SERVER = 'Server'
    SHARED = 'Shared'


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

    return description


def parse_get_function_code(data: str) -> str:
    SELECT_CODE_REGEX = re.compile(r'<syntaxhighlight[^>]*>(.+)</syntaxhighlight>')
    return re.search(SELECT_CODE_REGEX, data).group(1)


def parse_get_function_signature(code: str) -> FunctionType:
    WORD_REGEX_END = re.compile(r'([a-zA-Z0-9]+)$')
    WORD_REGEX = re.compile(r'([a-zA-Z0-9]+)')

    bracket_start = code.index('(')
    before_bracket = code[:bracket_start].strip()
    after_bracket = code[bracket_start + 1:].strip()

    name_regex = re.search(WORD_REGEX_END, before_bracket)  # last word before the opening bracket is function name
    function_name = name_regex.group(1)

    return_types_str = before_bracket[:name_regex.start()]
    return_types = [t.strip() for t in return_types_str.split(' ') if t.strip() != '']

    args: List[FunctionArgument] = []
    optional_arg = False
    for arg_signature in after_bracket.split(','):
        if arg_signature == ')':
            break  # No args

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
    data = data[re.search(START_REGEX, data).start():]

    docs: Dict[str, str] = dict()
    for line in data.split('\n'):
        if line == '':
            continue

        if line.strip().startswith('='):
            if 'argument' not in line.lower():
                break
            else:
                continue

        name_regex = re.search(r"\* *'+([^':]+):?'+", line)
        name = name_regex.group(1)

        line = line[name_regex.end():].strip()
        line = re.sub(r'[\[\]\'\"]', '', line)

        docs[name] = line

    return docs


def parse_get_function_returns() -> str:
    pass


def parse_get_function_type(data: str) -> ParseFunctionType:
    for line in data.split('\n'):
        line = line.strip().lower()
        if not line.startswith('{{'):
            continue

        if 'client function' in line:
            return ParseFunctionType.CLIENT
        if 'server function' in line:
            return ParseFunctionType.SERVER
        if 'server client function' in line:
            return ParseFunctionType.SHARED # TODO: is there two sections?

    raise RuntimeError('Cannot find function type')


def parse_apply_branches_and_bounds(data: str) -> str:
    END_CUTOFF_REGEX = re.compile(r'=+(See Also|Example)=+', re.IGNORECASE)
    regexp_result = re.search(END_CUTOFF_REGEX, data)
    if regexp_result:
        data = data[:regexp_result.start()]  # Cutoff

    return data


def get_function_data(f: FunctionUrl):
    url = f'{HOST_URL}/index.php?title={f.name[0].upper() + f.name[1:]}&action=edit'
    req = requests.request('GET', url)
    html = req.text
    soup_wiki = BeautifulSoup(html, 'html.parser')
    source_field = soup_wiki.select_one('#wpTextbox1')
    media_wiki = source_field.contents[0]

    return media_wiki
