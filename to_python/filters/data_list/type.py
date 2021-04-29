from to_python.core.filter import FilterAbstract
from to_python.filters.data_list.init import FilterFileOpenMixin


class FilterParseType(FilterAbstract, FilterFileOpenMixin):

    def parse_file(self, name: str, filepath: str):
        compound = self.context.parsed[name]
        text = self.read_file(filepath)

    def apply(self):
        for name, file in self.context.functions:
            self.parse_file(name, file)
