import os
from typing import List, Optional

from dump.shared import DATA as SHARED_DATA
from dump.client import DATA as CLIENT_DATA
from dump.server import DATA as SERVER_DATA
from src.fetch.function import CompoundFunctionData, FunctionData


# TODO: Looks like piece of script. Refactor that to readable code....

def init_dir(dir_name: str):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)


def init_workspace():
    init_dir('output/types/client')
    init_dir('output/types/shared')
    init_dir('output/types/server')


def prepare_type(source_type: str) -> str:
    if source_type == 'int' or source_type == 'float' or source_type == 'uint':
        return 'number'
    if source_type == 'str':
        return 'string'
    if source_type == 'bool':
        return 'boolean'
    if source_type == 'bool':
        return 'boolean'
    if source_type == 'var':
        return 'any'
    if source_type == 'mixed':
        return 'string'
    if source_type == 'function' or source_type == 'handle' or source_type == 'callback':
        return 'HandleFunction'

    return source_type


FILE_STARTER = dict(server='import {account, acl, aclgroup,' \
                           ' player, table, ban, blip,colshape,' \
                           'element,ped,pickup,resource,team,textdisplay,' \
                           'vehicle,xmlnode,textitem,HandleFunction,file,' \
                           'marker,radararea,request,userdata,timer,' \
                           'water} from "mtasa/server/structures";\n',
                    shared='import {account, acl, aclgroup,' \
                           ' player, table, ban, blip,colshape,' \
                           'element,ped,pickup,resource,team,textdisplay,' \
                           'vehicle,xmlnode,textitem,HandleFunction,file,' \
                           'marker,radararea,request,userdata,timer,' \
                           'water} from "mtasa/shared/structures";\n',
                    client='import {account, acl, aclgroup,' \
                           ' player, table, ban, blip,colshape,' \
                           'element,ped,pickup,resource,team,textdisplay,' \
                           'vehicle,xmlnode,textitem,HandleFunction,file,' \
                           'marker,radararea,request,userdata,timer,' \
                           'water} from "mtasa/client/structures";\n',
                    )


def docs_string(data: FunctionData) -> str:
    docs = '    /**\n'
    for line in data.docs.description.split('\n'):
        docs += '     * ' + line + '\n'
    for arg in data.signature.arguments:
        if arg.name not in data.docs.arguments:
            continue
        docs += '     * @param ' + arg.name + ' ' \
                + data.docs.arguments[arg.name].replace('\n', '  ') + '\n'
        if arg.default_value:
            docs += '     * @default ' + arg.default_value + '\n'
    for line in data.docs.result.split('\n'):
        docs += '     * @return ' + line + '\n'
    docs += '     */\n'

    return docs


def signature_string(data: FunctionData) -> str:
    signature = data.signature
    if len(signature.return_types) == 1:
        return_type = prepare_type(signature.return_types[0])
    else:
        type_list = [prepare_type(i) for i in signature.return_types]
        return_type = f'LuaMultiReturn<[{",".join(type_list)}]>'

    arguments = ''
    for arg in signature.arguments:
        arg_name = arg.name
        if arg_name == 'default':
            arg_name = 'defaultValue'
        arguments += f'{arg_name}{"?" if arg.optional and not "..." in arg.name else ""}' \
                     f': {prepare_type(arg.argument_type)}, '

    return f'    export function {signature.name}({arguments}): {return_type};\n\n'


def typescript_functions(data_list: List[CompoundFunctionData], key: str, dir_path: str):
    with open(f'{dir_path}/function.d.ts', 'w', encoding='UTF-8') as file:
        file.write(FILE_STARTER[key])
        file.write(f"declare module 'mtasa/{key}/functions' " + "{\n\n")

        for f in data_list:
            if f.server and 'utf8.' in f.server.signature.name:
                continue  # skip utf8 functions

            if f.server == f.client and key != 'shared':
                print(f'[INFO] Function {f.server.signature.name} skipped, because it is Shared')
                continue

            data: Optional[FunctionData] = getattr(f, key if key != 'shared' else 'server')

            file.write(docs_string(data))
            file.write(signature_string(data))

        file.write("}")


def utf8_functions():
    with open(f'output/types/shared/utf8.d.ts', 'w', encoding='UTF-8') as file:
        file.write(FILE_STARTER['shared'])
        file.write(f"declare module 'mtasa/shared/utf8' " + "{\n"
                                                            "    export namespace utf8 {\n\n")

        for f in SHARED_DATA:
            if not (f.server and 'utf8.' in f.server.signature.name):
                continue

            data: Optional[FunctionData] = f.server
            data.signature.name = data.signature.name.replace('utf8.', '')

            file.write(docs_string(data))
            file.write(signature_string(data))

        file.write("    }\n}\n")


if __name__ == '__main__':
    init_workspace()

    typescript_functions(SERVER_DATA + SHARED_DATA, 'server', 'output/types/server')
    typescript_functions(CLIENT_DATA + SHARED_DATA, 'client', 'output/types/client')
    typescript_functions(SHARED_DATA, 'shared', 'output/types/shared')

    utf8_functions()
