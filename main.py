import os
from typing import Optional

from src.fetch.fetch_function import get_function_data
from src.fetch.fetch_function_list import get_function_list
from src.fetch.function import ListType

WRITE_TO = 'client.py'

START_FROM: Optional[str] = 'xmlNodeGetName'

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
}

if __name__ == '__main__':
    f_list = get_function_list(ListType.CLIENT)
    write = START_FROM is None

    file_path = f'dump/{WRITE_TO}'
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='UTF-8') as file:
            file.write('from src.fetch.function import CompoundFunctionData, FunctionData,'
                       ' FunctionArgument, ListType, FunctionUrl, \\\n FunctionType, FunctionDoc, FunctionOOP\n\n')

    with open(file_path, 'a', encoding='UTF-8') as file:
        for index, f in enumerate(f_list):
            if f.name in BLACKLIST:
                continue

            if f.name == START_FROM and not write:
                write = True
            if not write:
                continue

            data = get_function_data(f)
            file.write(str(data))
            file.write('\n')

    print('[INFO] Complete')
