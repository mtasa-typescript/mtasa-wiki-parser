from crawler.core.filter import FilterAbstract
from crawler.core.types import FunctionUrl


class FilterRemoveDuplicates(FilterAbstract):
    def filter_predicate(self):
        def predicate(source: FunctionUrl):
            for url in self.context.url_list:
                if url.url == source.url:
                    return False

            return True

        return

    def apply(self):
        filtered = filter(lambda u: u, self.context.url_list)
        self.context.url_list
