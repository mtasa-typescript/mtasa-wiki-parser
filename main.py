import os
from typing import Optional

from src.fetch.fetch_function import get_function_data
from src.fetch.fetch_function_list import get_function_list
from src.fetch.function import ListType

# User values
FUNCTION_LIST: ListType = ListType.CLIENT  # What wiki function list will be used
SKIP_SHARED: bool = True  # Should the parser skip shared functions? (If they are already parsed and dumped)
START_FROM: Optional[str] = \
    None  # What function will be the pivot. Set None to start from the beginning
USE_CACHE: bool = True  # Use (or create) cache in dump-html directory

# File names
WRITE_CLIENT_TO = 'client.py'
WRITE_SERVER_TO = 'server.py'
WRITE_SHARED_TO = 'shared.py'

# Functions with non-standard wiki pages
BLACKLIST = {
    'dxCreateShader',
    'dxDrawImage',
    'Matrix',
    'Vector/Vector2',
    'Vector/Vector3',
    'Vector/Vector4',
    'call',
    'setTimer',
    'utf8.lower',
    'utf8.upper',
    'setWaterLevel',
    'setWeaponAmmo',

    'hasObjectPermissionTo',
    'httpClear',
    'httpRequestLogin',
    'httpSetResponseCode',
    'httpSetResponseCookie',
    'httpSetResponseHeader',
    'httpWrite',
}


def init_file(filepath: str):
    if not os.path.exists(filepath):
        with open(filepath, 'w', encoding='UTF-8') as init_file:
            init_file.write('from src.fetch.function import CompoundFunctionData, FunctionData,'
                            ' FunctionArgument, ListType, FunctionUrl, \\\n FunctionType, FunctionDoc, FunctionOOP\n\n')


def main():
    f_list = get_function_list(FUNCTION_LIST)  # Change this (client/server)
    write_to = WRITE_CLIENT_TO if FUNCTION_LIST == ListType.CLIENT else WRITE_SERVER_TO
    write = START_FROM is None

    file_path = f'dump/{write_to}'
    shared_file_path = f'dump/{WRITE_SHARED_TO}'
    init_file(file_path)
    init_file(shared_file_path)

    with open(file_path, 'w', encoding='UTF-8') as file:
        file.write(f"""from src.fetch.function import CompoundFunctionData, FunctionData, FunctionArgument, ListType, FunctionUrl, \\
 FunctionType, FunctionDoc, FunctionOOP

DATA = [
""")

        with open(shared_file_path, 'w', encoding='UTF-8') as shared_file:
            for index, f in enumerate(f_list):
                if f.name in BLACKLIST:
                    continue

                if f.name == START_FROM and not write:
                    write = True
                if not write:
                    continue

                data = get_function_data(f, SKIP_SHARED, USE_CACHE)
                if data:
                    if data.client is not None and data.server is not None:
                        shared_file.write(str(data))
                        shared_file.write(',\n')
                    else:
                        file.write(str(data))
                        file.write(',\n')
                else:
                    print(f'[WARN] Function {f.name} was not parsed. Maybe skipped')

        file.write(']\n')

    print('[INFO] Complete, final')


if __name__ == '__main__':
    main()
