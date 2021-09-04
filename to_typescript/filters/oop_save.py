import os
from copy import deepcopy, copy
from typing import List

from to_typescript.core.filter import FilterAbstract
from to_typescript.core.transform.extra_rules import ClassInheritance
from to_typescript.filters.function_save import FilterFunctionSave


class FilterOOPSave(FilterAbstract):
    FILE_STARTER = FilterFunctionSave.FILE_STARTER
    DUMP_FOLDERS = dict(server='output/server/oop',
                        client='output/client/oop',
                        client_gui='output/client/oop/gui')

    imports = FilterFunctionSave.imports

    @staticmethod
    def shift_lines(text: str, spaces: int) -> str:
        return '\n'.join(
            ' ' * spaces + line if line else line
            for line in text.split('\n')
        )

    def __init__(self):
        super().__init__()

        self.imports = deepcopy(self.imports)
        for key in self.imports['shared']:
            self.imports['client'].append(key)
            self.imports['server'].append(key)

    @staticmethod
    def get_class_begin(class_name: str, generic_string: str) -> str:
        inherit = ClassInheritance(class_name).get_child()
        if inherit:
            inherit_inline = f' extends {inherit}'
        else:
            inherit_inline = ''

        return f'''
/** @customConstructor {class_name} */
export class {class_name}{generic_string}{inherit_inline} {{
'''

    @staticmethod
    def get_class_end() -> str:
        return '}\n'

    def save_file_category(self,
                           class_name: str, side: str,
                           fields: List[str],
                           methods: List[str],
                           class_templates: List[str]):
        if not fields and not methods:
            return

        is_gui = class_name.startswith('Gui')
        cache_file = os.path.join(
            self.DUMP_FOLDERS[side + ('_gui' if is_gui else '')],
            f'{class_name}.d.ts'
        )

        imports: List[str] = deepcopy(self.imports[side])
        if class_name in imports:
            imports.remove(class_name)

        class_started = self.get_class_begin(class_name,
                                             '\n'.join(class_templates))

        text = (
                self.FILE_STARTER +
                FilterFunctionSave.generate_imports(imports, ('../' if is_gui else '') + '../structure') +
                class_started
        )
        if fields:
            text += self.shift_lines('\n\n'.join(fields), 4) + '\n\n'
        if methods:
            text += self.shift_lines('\n\n'.join(methods), 4) + '\n'
        text += self.get_class_end()

        with open(cache_file, 'w', encoding='UTF-8', newline='\n') as cache:
            cache.write(text)

    def apply(self):
        for key in self.DUMP_FOLDERS:
            folder = self.DUMP_FOLDERS[key]
            if not os.path.exists(folder):
                os.mkdir(folder)

        # TODO: move into Context method
        keys = set(self.context.declarations.oop_methods.keys())
        keys.update(set(self.context.declarations.oop_fields.keys()))

        for key in sorted(keys):
            for side in ['client', 'server']:
                self.save_file_category(
                    class_name=key,
                    side=side,
                    fields=self.context.declarations.oop_fields[key].get(side, []),
                    methods=self.context.declarations.oop_methods[key].get(side, []),
                    class_templates=self.context.declarations.oop_class_templates[key].get(side, []),
                )

        print('Generated .d.ts files with OOP\u001b[0m')
