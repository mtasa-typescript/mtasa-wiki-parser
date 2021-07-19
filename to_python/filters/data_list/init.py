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
        super().__init__()
        self.context_type = context_type

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
        context = getattr(self.context, self.context_type)
        for name in context.pages:
            filepath = context.pages[name]
            context.parsed[name] = self.initialize_parsed_value()
            context.raw_data[name] = self.read_file(filepath)
