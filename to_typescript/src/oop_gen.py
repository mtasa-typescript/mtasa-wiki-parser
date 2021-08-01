from src.fetch.function import FunctionData
from to_typescript.src.function_gen import prepare_type, prepare_arg_name


def prepare_class_name(name: str) -> str:
    if prepare_type(name.lower()) != name.lower():
        return prepare_type(name.lower())

    return prepare_type(name)


def oop_docs(data: FunctionData) -> str:
    functional_name = data.signature.name
    return '    /**\n     * @see {@link ' + functional_name + '}\n     */\n'


def property_definition(data: FunctionData) -> str:
    signature = data.signature
    if len(signature.return_types) == 1:
        prop_type = prepare_type(signature.return_types[0])
    else:
        type_list = [prepare_type(i) for i in signature.return_types]
        prop_type = f'LuaMultiReturn<[{",".join(type_list)}]>'

    return f'    {data.oop.field}: {prop_type};\n'


def method_definition(data: FunctionData) -> str:
    signature = data.signature
    if len(signature.return_types) == 1:
        return_type = prepare_type(signature.return_types[0])
    else:
        type_list = [prepare_type(i) for i in signature.return_types]
        return_type = f'LuaMultiReturn<[{",".join(type_list)}]>'

    arguments = ''
    for index, arg in enumerate(signature.arguments):
        arg_type = prepare_type(arg.argument_type)
        if index == 0 and data.oop.class_name.lower() in arg_type.lower():
            continue

        arg_name = prepare_arg_name(arg.name)

        arguments += f'{arg_name}{"?" if arg.optional and not "..." in arg.name else ""}' \
                     f': {arg_type}, '

    return f'    {data.oop.method_name}({arguments}): {return_type};\n'

class TypeScriptOOPGen:
    pass