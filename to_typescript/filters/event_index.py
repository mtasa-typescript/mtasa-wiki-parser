import os

from to_typescript.core.filter import FilterAbstract
from to_typescript.filters.function_declarations import FilterGenerateFunctionDeclarations
from to_typescript.filters.function_save_index import FilterFunctionSaveIndex


class FilterEventSaveIndex(FilterAbstract):
    """
    Saves root event.d.ts file
    Appends event info into mtasa.d.ts files
    """

    DUMP_FOLDERS = FilterFunctionSaveIndex.DUMP_FOLDERS
    FILE_NAME = FilterFunctionSaveIndex.FILE_NAME
    EVENT_FILE_NAME = 'event.d.ts'

    FILE_STARTER = '''// Autogenerated file.
// DO NOT EDIT. ANY CHANGES WILL BE OVERWRITTEN

'''

    def save_file_event(self, side: str):
        text = self.FILE_STARTER
        cache_file = os.path.join(FilterEventSaveIndex.DUMP_FOLDERS[side],
                                  FilterEventSaveIndex.EVENT_FILE_NAME)

        category_list = self.context.events_declarations.keys()
        for category in sorted(category_list):
            data = self.context.events_declarations[category]
            if not data[side]:
                continue

            filename = FilterGenerateFunctionDeclarations.get_dts_file_name(category)
            path = f'./event/{filename}'
            text += FilterFunctionSaveIndex.generate_exports(path) + '\n'

        with open(cache_file, 'w', encoding='UTF-8', newline='\n') as cache:
            cache.write(text)

    @staticmethod
    def append_index(side):
        cache_file = os.path.join(FilterEventSaveIndex.DUMP_FOLDERS[side],
                                  FilterEventSaveIndex.FILE_NAME)
        with open(cache_file, 'a', encoding='UTF-8', newline='\n') as cache:
            cache.write('''
export { EventNames } from './event/all_event_names';
import * as Event from './event';
export { Event };
''')

    def apply(self):
        for side in ['client', 'server']:
            FilterEventSaveIndex.append_index(side)

        print(f'Append event data into {self.FILE_NAME} (index file)')

        for side in ['client', 'server']:
            self.save_file_event(side)

        print(f'Generate event.d.ts files')
