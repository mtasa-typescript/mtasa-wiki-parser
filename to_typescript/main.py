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
    init_dir('output/types/client')
    init_dir('output/types/shared')
    init_dir('output/types/server')


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
                           'water,iterator} from "mtasa/shared/structures";\n',
                    client='import {account, acl, aclgroup,' \
                           ' player, table, ban, blip,colshape,' \
                           'element,ped,pickup,resource,team,textdisplay,' \
                           'vehicle,xmlnode,textitem,HandleFunction,file,' \
                           'marker,radararea,request,userdata,timer,' \
                           'water,browser,progressBar,light,effect,'
                           'gui,searchlight,weapon,guibrowser,'
                           'txd,dff,col,ifp,primitiveType,guiscrollbar,'
                           'guimemo,texture,objectgroup,projectile,Matrix,'
                           '} from "mtasa/client/structures";\n',
                    )

FUNCTION_BLACKLIST: Dict[str, Set[str]] = {
    'server': {
        '',
    },
    'client': {
        '',
    },
    'shared': {
        'utf8.byte',
        'utf8.lower',
        'utf8.match',
    },
}


def function_file_gen(data_list: List[CompoundFunctionData], key: str, dir_path: str):
    # This function ignores Blacklist

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


def function_file_replace(data_list: List[CompoundFunctionData], key: str, dir_path: str):
    with open(f'{dir_path}/function.d.ts', 'r', encoding='UTF-8') as file:
        file_data = file.read()

    for f in data_list:
        if f.server and 'utf8.' in f.server.signature.name:
            continue  # skip utf8 functions

        if f.server == f.client and key != 'shared':
            print(f'[INFO] Function {f.server.signature.name} skipped, because it is Shared')
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
    with open(f'output/types/shared/utf8.d.ts', 'w', encoding='UTF-8') as file:
        file.write(FILE_STARTER['shared'])
        file.write(f"declare module 'mtasa/shared/utf8' " + "{\n"
                                                            "    export namespace utf8 {\n\n")

        for f in SHARED_DATA:
            if not (f.server and 'utf8.' in f.server.signature.name):
                continue

            data: Optional[FunctionData] = f.server
            if data.signature.name in FUNCTION_BLACKLIST['shared']:
                continue

            data.signature.name = data.signature.name.replace('utf8.', '')

            file.write(docs_string(data))
            file.write(signature_string(data) + '\n')

        file.write("    }\n}\n")


if __name__ == '__main__':
    init_workspace()

    typescript_functions(SERVER_DATA + SHARED_DATA, 'server', 'output/types/server')
    typescript_functions(CLIENT_DATA + SHARED_DATA, 'client', 'output/types/client')
    typescript_functions(SHARED_DATA, 'shared', 'output/types/shared')

    # utf8_functions() # TODO FIXME: fix replace
