import os
from typing import List

from to_python.core.types import EventData
from to_typescript.core.filter import FilterAbstract


class FilterEventSaveNames(FilterAbstract):
    """
    Generate enum with event names
    """

    FILE_STARTER = '''// Autogenerated file.
// DO NOT EDIT. ANY CHANGES WILL BE OVERWRITTEN

'''

    DUMP_FOLDERS = dict(server='output/server/event',
                        client='output/client/event')

    @staticmethod
    def normalize_enum_variable_name(name: str) -> str:
        return name[0].upper() + name[1:]

    @staticmethod
    def generate_file_content(data_list: List[List[EventData]]) -> str:
        """
        Generated .d.ts with enum with all event names
          (for client / server side)
        """
        result = FilterEventSaveNames.FILE_STARTER
        result += 'export const enum EventNames {\n'

        for data in data_list:
            variable_name = FilterEventSaveNames.normalize_enum_variable_name(
                data[0].name
            )
            result += f'    {variable_name} = \'{data[0].name}\',\n'

        result += '}\n'

        return result

    @staticmethod
    def save_file(folder: str, content: str):
        path = os.path.join(folder, 'all_event_names.d.ts')

        with open(path, 'w', encoding='UTF-8', newline='\n') as cache:
            cache.write(content)

    def apply(self):
        for side in ['client', 'server']:
            all_events_by_side: List[List[EventData]] = []
            for category in self.context.events_declarations:
                data: List[List[EventData]] = \
                    self.context.events_declarations[category][side]
                if not data:
                    continue

                all_events_by_side.extend(data)

            content = self.generate_file_content(all_events_by_side)
            self.save_file(
                folder=self.DUMP_FOLDERS[side],
                content=content,
            )

        print('Generated event name declaration files\u001b[0m')
