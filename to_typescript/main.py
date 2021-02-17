import os
from typing import List, Optional, Dict, Set

from dump.shared import DATA as SHARED_DATA
from dump.client import DATA as CLIENT_DATA
from dump.server import DATA as SERVER_DATA
from src.fetch.function import CompoundFunctionData, FunctionData

from to_typescript.src.function_gen import docs_string, signature_string, find_function_in_file


# TODO: Looks like piece of script. Refactor that to readable code....

def init_dir(dir_name: str):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)


def init_workspace():
    init_dir('output/types/mtasa/client')
    init_dir('output/types/mtasa/shared')
    init_dir('output/types/mtasa/server')


FILE_STARTER = dict(server='/// <reference types="typescript-to-lua/language-extensions" />\n'
                           'import {account, acl, aclgroup,' \
                           ' player, table, ban, blip,colshape,' \
                           'element,ped,pickup,resource,team,textdisplay,' \
                           'vehicle,xmlnode,textitem,HandleFunction,file,' \
                           'marker,radararea,request,userdata,timer,' \
                           'water} from "./structure";\n',
                    shared='/// <reference types="typescript-to-lua/language-extensions" />\n'
                           'import {account, acl, aclgroup,' \
                           ' player, table, ban, blip,colshape,' \
                           'element,ped,pickup,resource,team,textdisplay,' \
                           'vehicle,xmlnode,textitem,HandleFunction,file,' \
                           'marker,radararea,request,userdata,timer,' \
                           'water,iterator} from "./structure";\n',
                    client='/// <reference types="typescript-to-lua/language-extensions" />\n'
                           'import {account, acl, aclgroup,' \
                           ' player, table, ban, blip,colshape,' \
                           'element,ped,pickup,resource,team,textdisplay,' \
                           'vehicle,xmlnode,textitem,HandleFunction,file,' \
                           'marker,radararea,request,userdata,timer,' \
                           'water,browser,progressBar,light,effect,'
                           'gui,searchlight,weapon,guibrowser,'
                           'txd,dff,col,ifp,primitiveType,guiscrollbar,'
                           'guimemo,texture,objectgroup,projectile,Matrix,'
                           '} from "./structure";\n',
                    )

FUNCTION_BLACKLIST: Dict[str, Set[str]] = {
    'server': {
        '',
    },
    'client': {
        'dxGetMaterialSize',  # Optional return type
        'guiGridListAddRow',  # Union type in argument
        'processLineOfSight',  # Comments in return types
    },
    'shared': {
        'utf8.byte',
        'utf8.match',
    },
}


def function_file_gen(data_list: List[CompoundFunctionData], key: str, dir_path: str):
    # This function ignores Blacklist

    with open(f'{dir_path}/function.d.ts', 'w', encoding='UTF-8') as file:
        file.write(FILE_STARTER[key])

        for f in data_list:
            if f.server and 'utf8.' in f.server.signature.name:
                continue  # skip utf8 functions

            if f.server == f.client and key != 'shared':
                print(f'[INFO] Function {f.server.signature.name} skipped, because it is Shared')
                continue

            if f.server != f.client and key == 'shared':
                print(f'[INFO] Shared function {f.server.signature.name} skipped, '
                      f'because it is non equal to server and client')
                continue

            data: Optional[FunctionData] = getattr(f, key if key != 'shared' else 'server')

            file.write(docs_string(data))
            file.write(signature_string(data))


def function_file_replace(data_list: List[CompoundFunctionData], key: str, dir_path: str):
    with open(f'{dir_path}/function.d.ts', 'r', encoding='UTF-8') as file:
        file_data = file.read()

    for f in data_list:
        if f.server and 'utf8.' in f.server.signature.name:
            continue  # skip utf8 functions

        if f.server == f.client and key != 'shared':
            print(f'[INFO] Function {f.server.signature.name} skipped, because it is Shared')
            continue

        if f.server != f.client and key == 'shared':
            print(f'[INFO] Shared function {f.server.signature.name} skipped, '
                  f'because it is non equal to server and client')
            continue

        data: Optional[FunctionData] = getattr(f, key if key != 'shared' else 'server')
        if data.signature.name in FUNCTION_BLACKLIST[key]:
            continue

        start_pos, end_pos = find_function_in_file(data.signature.name, file_data)
        data_to_replace = docs_string(data) + signature_string(data)

        file_data = file_data[:start_pos] + data_to_replace + file_data[end_pos:]

    with open(f'{dir_path}/function.d.ts', 'w', encoding='UTF-8') as file:
        file.write(file_data)


def typescript_functions(data_list: List[CompoundFunctionData], key: str, dir_path: str):
    if os.path.exists(f'{dir_path}/function.d.ts'):
        return function_file_replace(data_list, key, dir_path)

    return function_file_gen(data_list, key, dir_path)


def utf8_functions():
    with open(f'output/types/mtasa/shared/utf8.d.ts', 'r', encoding='UTF-8') as file:
        file_data = file.read()

    with open(f'output/types/mtasa/shared/utf8.d.ts', 'w', encoding='UTF-8') as file:
        file.write(FILE_STARTER['shared'])
        file.write("export namespace utf8 {\n")

        for f in SHARED_DATA:
            if not (f.server and 'utf8.' in f.server.signature.name):
                continue

            data: Optional[FunctionData] = f.server
            if data.signature.name in FUNCTION_BLACKLIST['shared']:  # If function in blacklist -- reveal existing data
                start_pos, end_pos = find_function_in_file(data.signature.name, file_data)
                file.write(file_data[start_pos:end_pos] + '\n')
                continue

            file.write(docs_string(data))
            file.write(signature_string(data, '') + '\n')

        file.write("}\n")


if __name__ == '__main__':
    init_workspace()

    print('[INFO] Server data gen')
    typescript_functions(SERVER_DATA + SHARED_DATA, 'server', 'output/types/mtasa/server')
    print('[INFO] Client data gen')
    typescript_functions(CLIENT_DATA + SHARED_DATA, 'client', 'output/types/mtasa/client')
    print('[INFO] Shared data gen')
    typescript_functions(SHARED_DATA, 'shared', 'output/types/mtasa/shared')

    print('[INFO] Shared utf8.* data gen')
    utf8_functions()
