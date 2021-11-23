import glob
import os
from typing import List

from to_python.core.filter import FilterAbstract


class FilterCollectDumpFiles(FilterAbstract):
    """
    Accumulates all files inside DUMP_DIRECTORY into context.functions
    """

    DUMP_DIRECTORY = dict(functions='../crawler/dump_html/functions/**',
                          events='../crawler/dump_html/events/**')

    @staticmethod
    def function_name(name: str):
        return name[0].lower() + name[1:]

    def get_file_list(self) -> List[str]:
        return [
            f for f in
            glob.iglob(self.DUMP_DIRECTORY[self.context_type], recursive=True)
            if os.path.isfile(f)
            if not f.endswith('.py')
            if not f.endswith('.gitignore')
            if '__pycache__' not in f
        ]

    def apply(self):
        for file in self.get_file_list():
            function_name = self.function_name(os.path.basename(file))

            # Skip function if it is not defined
            # in the __init__.py declaration list
            if function_name not in self.context_data.urls:
                continue

            self.context_data.pages[self.function_name(function_name)] = file

        print(
            f'Collected HTML files (context '
            f'\u001b[34m{self.context_type}\u001b[0m): \u001b[34m'
            f'{len(self.context_data.pages)}\u001b[0m items\u001b[0m'
        )
