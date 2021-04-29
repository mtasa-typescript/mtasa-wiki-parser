import os
import glob
from typing import List

from to_python.core.filter import FilterAbstract


class FilterCollectDumpFiles(FilterAbstract):
    DUMP_DIRECTORY = '../crawler/dump-html/**'

    @staticmethod
    def function_name(name: str):
        return name[0].lower() + name[1:]

    def get_file_list(self) -> List[str]:
        return [f for f in glob.iglob(self.DUMP_DIRECTORY, recursive=True)
                if os.path.isfile(f)]

    def apply(self):
        for file in self.get_file_list():
            function_name = os.path.basename(file)
            self.context.functions[self.function_name(function_name)] = file
