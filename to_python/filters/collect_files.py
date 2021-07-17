import glob
import os
from typing import List

from to_python.core.filter import FilterAbstract


class FilterCollectDumpFiles(FilterAbstract):
    """
    Accumulates all files inside DUMP_DIRECTORY into context.functions
    """

    DUMP_DIRECTORY = '../crawler/dump_html/functions/**'

    @staticmethod
    def function_name(name: str):
        return name[0].lower() + name[1:]

    def get_file_list(self) -> List[str]:
        return [
            f for f in glob.iglob(self.DUMP_DIRECTORY, recursive=True)
            if os.path.isfile(f)
            if not f.endswith('.py')
            if not f.endswith('.gitignore')
            if '__pycache__' not in f
        ]

    def apply(self):
        for file in self.get_file_list():
            function_name = os.path.basename(file)
            self.context.functions[self.function_name(function_name)] = file

        print(f'Collected HTML files: {len(self.context.functions)} items')
