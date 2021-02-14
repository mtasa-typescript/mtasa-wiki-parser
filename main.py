import os
from typing import Optional

from src.fetch.fetch_function import get_function_data
from src.fetch.fetch_function_list import get_function_list
from src.fetch.function import ListType

WRITE_TO = 'client.py'
WRITE_SHARED_TO = 'shared.py'

START_FROM: Optional[str] = 'isWorldSoundEnabled'

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


if __name__ == '__main__':
    f_list = get_function_list(ListType.CLIENT)  # Change this (client/server)
    write = START_FROM is None

    file_path = f'dump/{WRITE_TO}'
    shared_file_path = f'dump/{WRITE_SHARED_TO}'
    init_file(file_path)
    init_file(shared_file_path)

    with open(file_path, 'a', encoding='UTF-8') as file:
        with open(shared_file_path, 'a', encoding='UTF-8') as shared_file:
            for index, f in enumerate(f_list):
                if f.name in BLACKLIST:
                    continue

                if f.name == START_FROM and not write:
                    write = True
                if not write:
                    continue

                data = get_function_data(f, True)  # Set True, to skip shared functions
                if data:
                    if data.client is not None and data.server is not None:
                        shared_file.write(str(data))
                        shared_file.write('\n')
                    else:
                        file.write(str(data))
                        file.write('\n')
                else:
                    print(f'[WARN] Function {f.name} was not parsed. Maybe skipped')

    print('[INFO] Complete, final')
