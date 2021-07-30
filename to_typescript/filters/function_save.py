import os
from copy import deepcopy
from typing import List, Dict

from to_typescript.core.filter import FilterAbstract


class FilterFunctionSave(FilterAbstract):
    FILE_STARTER = '''// Autogenerated file.
// DO NOT EDIT. ANY CHANGES WILL BE OVERWRITTEN

'''
    DUMP_FOLDERS = dict(server='output/types/mtasa/server/function',
                        client='output/types/mtasa/client/function')

    imports = dict(
        server=[
            'TextDisplay',
            'Account',
            'ACL',
            'ACLGroup',
            'Ban',
            'XML',
        ],
        client=[
            'ProgressBar',
            'Gui',
            'EngineTXD',
            'EngineDFF',
            'EngineCOL',
            'EngineIFP',
            'PrimitiveType',
            'DxTexture',
            'ObjectGroup',
            'Matrix',
            'Browser',
            'Light',
            'Effect',
            'Searchlight',
            'Weapon',
            'GuiBrowser',
            'GuiMemo',
            'GuiElement',
            'GuiEdit',
            'GuiScrollBar',
            'GuiWindow',
            'Projectile',
            'Material',
        ],
        shared=[  # Appends to client/server list in runtime
            'Userdata',
            'TextItem',
            'Pickup',
            'Request',
            'Player',
            'Blip',
            'ColShape',
            'Element',
            'Ped',
            'Resource',
            'Team',
            'Vehicle',
            'XmlNode',
            'File',
            'Marker',
            'MTASAObject',
            'RadarArea',
            'Water',
            'Timer',
            'HandleFunction',
            'TimerCallbackFunction',
            'FetchRemoteCallback',
            'GenericEventHandler',
            'CommandHandler',
        ]
    )

    def __init__(self):
        super().__init__()

        self.imports = deepcopy(self.imports)
        for key in self.imports['shared']:
            self.imports['client'].append(key)
            self.imports['server'].append(key)

    @staticmethod
    def generate_imports(module_list: List[str], filename: str) -> str:
        modules = ',\n    '.join(module_list)
        return f'''import {{
    {modules}
}} from '{filename}';
'''

    def save_file_category(self, category_name: str, side: str, content: List[str]):
        cache_file = os.path.join(self.DUMP_FOLDERS[side], f'{category_name}.d.ts')

        text = (self.FILE_STARTER +
                self.generate_imports(self.imports[side], '../structure')
                + '\n')
        text += '\n\n'.join(content) + '\n'

        with open(cache_file, 'w', encoding='UTF-8', newline='\n') as cache:
            cache.write(text)

    @staticmethod
    def create_dump_directories(directories: Dict[str, str]):
        """
        Creates a directory if the directory does not exists
        """
        for key in directories:
            folder = directories[key]
            if not os.path.exists(folder):
                os.mkdir(folder)

    def apply(self):
        self.create_dump_directories(self.DUMP_FOLDERS)

        functions = self.context.declarations.function
        for category_name in functions:
            for side in functions[category_name]:
                self.save_file_category(category_name=category_name,
                                        side=side,
                                        content=functions[category_name][side])

        print('Generated .d.ts files with functions')
