from to_python.core.filter import FilterAbstract
from to_python.core.types import CompoundFunctionData, CompoundEventData


class FilterInitInternalList(FilterAbstract):
    """
    Initializes context.parsed and fills context.raw_data
    """

    def __init__(self, context_type: str):
        """
        :param context_type: `functions` or `events`
        """
        super().__init__(context_type)

    @staticmethod
    def read_file(filepath: str) -> str:
        with open(filepath, encoding='UTF-8', newline='\n') as file:
            return file.read()

    def initialize_parsed_value(self):
        if self.context_type == 'events':
            return CompoundEventData()
        if self.context_type == 'functions':
            return CompoundFunctionData()

    def apply(self):
        for name in self.context_data.pages:
            filepath = self.context_data.pages[name]
            self.context_data.parsed[name] = self.initialize_parsed_value()
            self.context_data.raw_data[name] = self.read_file(filepath)

        print('Internal list init complete\u001b[0m')
