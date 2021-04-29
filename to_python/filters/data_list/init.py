from to_python.core.filter import FilterAbstract
from to_python.core.types import CompoundFunctionData


class FilterInitInternalList(FilterAbstract):
    """
    Initializes context.parsed and fills context.raw_data
    """

    @staticmethod
    def read_file(filepath: str) -> str:
        with open(filepath, encoding='UTF-8') as file:
            return file.read()

    def apply(self):
        for name in self.context.functions:
            filepath = self.context.functions[name]
            self.context.parsed[name] = CompoundFunctionData()
            self.context.raw_data[name] = self.read_file(filepath)
