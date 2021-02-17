import re

from src.fetch.function import FunctionData


def prepare_type(source_type: str) -> str:
    TYPE_ALIASES = {
        'gui-browser': 'guibrowser',
        'gui-scrollbar': 'guiscrollbar',
        'gui-memo': 'guimemo',
        'matrix': 'Matrix',
    }
    if source_type == 'int' or source_type == 'float' or source_type == 'uint' or source_type == 'color':
        return 'number'
    if source_type == 'str':
        return 'string'
    if source_type == 'bool':
        return 'boolean'
    if source_type == 'bool':
        return 'boolean'
    if source_type == 'var' or source_type == 'value':
        return 'any'
    if source_type == 'nil':
        return 'null'
    if source_type == 'mixed':
        return 'string'
    if source_type == 'function' or source_type == 'handle' or source_type == 'callback':
        return 'HandleFunction'

    if source_type in TYPE_ALIASES:
        return TYPE_ALIASES[source_type]

    source_type = source_type.replace('/', '|')
    union_types = source_type.split('|')
    if len(union_types) > 1:
        union_types = [prepare_type(t) for t in union_types]
        source_type = '|'.join(union_types)

    return source_type


def prepare_arg_name(name: str) -> str:
    if name == 'default':
        return 'defaultValue'
    if name == 'var':
        return 'variableValue'

    return name


def docs_post_processing(docs: str) -> str:
    MAX_LINE_LENGTH = 100

    lines = docs.split('\n')
    new_lines = []

    for line in lines:
        new_line = ''
        i = 0

        for i in range(MAX_LINE_LENGTH, len(line), MAX_LINE_LENGTH):
            partial_docs = line[i - MAX_LINE_LENGTH:i]
            new_line += '\n* '.join(partial_docs.rsplit(' ', 1))

        if i < len(line):
            new_line += line[i:]

        new_lines.append(new_line)

    return '\n'.join(new_lines)


def docs_string(data: FunctionData) -> str:
    docs = '/**\n'

    for line in data.docs.description.split('\n'):
        docs += ' * ' + line + '\n'
    docs += ' * @see {@link https://wiki.multitheftauto.com/wiki/' + data.signature.name + '|MTASA Wiki}\n'

    for arg in data.signature.arguments:
        if arg.name not in data.docs.arguments:
            continue
        docs += ' * @param ' + arg.name + ' ' \
                + data.docs.arguments[arg.name].replace('\n', '  ') + '\n'
        if arg.default_value:
            docs += ' * @default ' + arg.default_value + '\n'

    for index, line in enumerate(data.docs.result.split('\n')):
        if index == 0:
            docs += ' * @return ' + line + '\n'
        else:
            docs += ' * * ' + line + '\n'

    docs += ' */\n'

    return docs_post_processing(docs)


def signature_string(data: FunctionData, pre_string: str = 'export') -> str:
    signature = data.signature
    if len(signature.return_types) == 1:
        return_type = prepare_type(signature.return_types[0])
    else:
        type_list = [prepare_type(i) for i in signature.return_types]
        return_type = f'LuaMultiReturn<[{",".join(type_list)}]>'

    arguments = ''
    for arg in signature.arguments:
        arg_name = prepare_arg_name(arg.name)

        arguments += f'{arg_name}{"?" if arg.optional and not "..." in arg.name else ""}' \
                     f': {prepare_type(arg.argument_type)}, '

    function_name = signature.name.split('.')[-1]
    return f'{pre_string} function {function_name}({arguments}): {return_type};\n'


def find_function_in_file(function_name: str, file_data: str) -> (int, int):
    function_name = function_name.split('.')[-1]
    regex = re.compile(rf'^ *\/\*\*\n(((?<!\/\*\*)[\S\s])+?)\*\/\n.+function ({function_name})\W[^;]+;\n', re.MULTILINE)
    result = regex.search(file_data)

    if not result:
        raise RuntimeError(f'Function definition for {function_name} not found. '
                           f'Please provide it or remove the whole file to regenerate it')

    return result.start(), result.end()
