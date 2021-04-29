import wikitextparser as wtp

from to_python.core.filter import FilterAbstract


class FilterWikiTextParser(FilterAbstract):
    def parse(self, code: str):
        parsed = wtp.parse(code)
        print(parsed)

    def apply(self):
        for f_name in self.context.raw_data:
            self.parse(self.context.raw_data[f_name])
