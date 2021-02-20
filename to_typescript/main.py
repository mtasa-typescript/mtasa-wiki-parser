import os
from collections import defaultdict
from typing import List, Optional, Dict, Set, DefaultDict

from dump.client import DATA as CLIENT_DATA
from dump.shared import DATA as SHARED_DATA
from src.fetch.function import CompoundFunctionData, FunctionData
from to_typescript.src.file_gen import prepare_category_file_name
from to_typescript.src.function_gen import docs_string, signature_string, find_function_in_file
from to_typescript.src.oop_gen import oop_docs, method_definition, property_definition, prepare_class_name


# TODO: Looks like piece of script. Refactor that to readable code....

def init_dir(dir_name: str):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)


def init_workspace():
    init_dir('output/types/mtasa/client')
    init_dir('output/types/mtasa/shared')
    init_dir('output/types/mtasa/server')
    init_dir('output/types/mtasa/client/oop')
    init_dir('output/types/mtasa/server/oop')
    init_dir('output/types/mtasa/client/function')
    init_dir('output/types/mtasa/server/function')


FILE_STARTER = dict(server='/// <reference types="typescript-to-lua/language-extensions" />\n'
                           '/** @noSelfInFile */\n\n'
                           'import {Account, ACL, ACLGroup,'
                           ' Player, Table, Ban, Blip,ColShape,'
                           'Element,Ped,Pickup,Resource,Team,TextDisplay,'
                           'Vehicle,XmlNode,TextItem,HandleFunction,File,'
                           'Marker,RadarArea,Request,Userdata,Timer,'
                           'Water} from "types/mtasa/server/structure";\n',

                    shared='/// <reference types="typescript-to-lua/language-extensions" />\n'
                           '/** @noSelfInFile */\n\n'
                           'import {iterator} from "types/mtasa/shared/structure";\n',

                    client='/// <reference types="typescript-to-lua/language-extensions" />\n'
                           '/** @noSelfInFile */\n\n'
                           'import {Account, ACL, ACLGroup,'
                           ' Player, Table, Ban, Blip,ColShape,'
                           'Element,Ped,Pickup,Resource,Team,TextDisplay,'
                           'Vehicle,XmlNode,TextItem,HandleFunction,File,'
                           'Marker,RadarArea,Request,Userdata,Timer,'
                           'Water,Browser,ProgressBar,Light,Effect,'
                           'Gui,Searchlight,Weapon,GuiBrowser,'
                           'Txd,Dff,Col,Ifp,PrimitiveType,GuiScrollBar,'
                           'GuiMemo,Texture,ObjectGroup,Projectile,Matrix,'
                           '} from "types/mtasa/client/structure";\n',
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


def should_function_be_skipped(data: FunctionData, key: str):
    if 'utf8.' in data.signature.name:
        return True  # skip utf8 functions

    return False


CategorizedType = DefaultDict[str, List[FunctionData]]


def categorize_functions(data_list: List[CompoundFunctionData], key: str) -> CategorizedType:
    categorized: CategorizedType = defaultdict(list)
    for f in data_list:
        data: Optional[FunctionData] = getattr(f, key)
        categorized[data.url.category].append(data)

    return categorized


def function_file_gen(categorized: CategorizedType, key: str, dir_path: str, category: str):
    # This function ignores Blacklist
    functions: Set[str] = set()

    file_name = prepare_category_file_name(category)
    with open(f'{dir_path}/function/{file_name}', 'w', encoding='UTF-8') as file:
        file.write(FILE_STARTER[key])

        for data in categorized[category]:
            if data.signature.name in functions:
                continue

            functions.add(data.signature.name)

            if should_function_be_skipped(data, key):
                continue

            file.write(docs_string(data))
            file.write(signature_string(data))


def function_file_replace(categorized: CategorizedType, key: str, dir_path: str, category: str):
    file_name = prepare_category_file_name(category)
    with open(f'{dir_path}/function/{file_name}', 'r', encoding='UTF-8') as file:
        file_data = file.read()

    for data in categorized[category]:
        if should_function_be_skipped(data, key):
            continue

        if data.signature.name in FUNCTION_BLACKLIST[key]:
            continue

        start_pos, end_pos = find_function_in_file(data.signature.name, file_data)
        data_to_replace = docs_string(data) + signature_string(data)

        file_data = file_data[:start_pos] + data_to_replace + file_data[end_pos:]

    with open(f'{dir_path}/function/{file_name}', 'w', encoding='UTF-8') as file:
        file.write(file_data)


def typescript_functions(data_list: List[CompoundFunctionData], key: str, dir_path: str):
    categorized = categorize_functions(data_list, key)

    for category in categorized:
        file_name = prepare_category_file_name(category)

        if os.path.exists(f'{dir_path}/function/{file_name}'):
            function_file_replace(categorized, key, dir_path, category)
        else:
            function_file_gen(categorized, key, dir_path, category)


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


def typescript_oop(data_list: List[CompoundFunctionData], key: str, dir_path: str):
    classes_data: DefaultDict[str, List[str]] = defaultdict(list)

    for f in data_list:
        data: Optional[FunctionData] = getattr(f, key)
        if should_function_be_skipped(data, key):
            continue

        if not data.oop:
            continue

        class_name = prepare_class_name(data.oop.class_name)
        put_entrypoint = classes_data[class_name]
        if data.oop.field and not data.oop.method_name.startswith('set'):
            field_line = property_definition(data) + '\n'
            if field_line not in put_entrypoint:
                put_entrypoint.append(oop_docs(data))
                put_entrypoint.append(field_line)

        method_line = method_definition(data) + '\n'
        if method_line not in put_entrypoint:
            put_entrypoint.append(oop_docs(data))
            put_entrypoint.append(method_line)

    for class_name in classes_data:
        path = os.path.join(dir_path, f'{class_name}.d.ts')
        if os.path.exists(path):
            print(f'\n[INFO] File {path} exists. Skipped')
            continue

        with open(path, 'w') as file:
            file.write(FILE_STARTER[key])
            file.write(f'export class {class_name} ' + '{\n')
            for line in classes_data[class_name]:
                file.write(line)

            file.write('\n}')


if __name__ == '__main__':
    init_workspace()

    # print('[INFO] Server data gen')
    # typescript_functions(SERVER_DATA + SHARED_DATA, 'server', 'output/types/mtasa/server')
    # print('[INFO] Client data gen')
    # typescript_functions(CLIENT_DATA + SHARED_DATA, 'client', 'output/types/mtasa/client')

    # print('[INFO] Shared utf8.* data gen')
    # utf8_functions()

    print('\n[INFO] OOP Code generation. Will be skipped, if files exists')
    # print('[INFO] Server data gen')
    # typescript_oop(SERVER_DATA + SHARED_DATA, 'server', 'output/types/mtasa/server/oop')
    print('[INFO] Client data gen')
    typescript_oop(CLIENT_DATA + SHARED_DATA, 'client', 'output/types/mtasa/client/oop')
