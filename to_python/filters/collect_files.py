import glob
import os
from typing import List

from to_python.core.context import ContextData
from to_python.core.filter import FilterAbstract


class FilterCollectDumpFiles(FilterAbstract):
    """
    Accumulates all files inside DUMP_DIRECTORY into context.functions
    """

    def __init__(self, context_type: str):
        """
        :param context_type: `functions` or `events`
        """
        super().__init__()

        self.context_type = context_type

    DUMP_DIRECTORY = dict(functions='../crawler/dump_html/functions/**',
                          events='../crawler/dump_html/events/**')

    @staticmethod
    def function_name(name: str):
        return name[0].lower() + name[1:]

    def get_file_list(self) -> List[str]:
        return [
            f for f in glob.iglob(self.DUMP_DIRECTORY[self.context_type], recursive=True)
            if os.path.isfile(f)
            if not f.endswith('.py')
            if not f.endswith('.gitignore')
            if '__pycache__' not in f
        ]

    def apply(self):
        context: ContextData = getattr(self.context, self.context_type)

        for file in self.get_file_list():
            function_name = os.path.basename(file)
            context.pages[self.function_name(function_name)] = file

        print(f'Collected HTML files (context {self.context_type}): {len(context.pages)} items')
