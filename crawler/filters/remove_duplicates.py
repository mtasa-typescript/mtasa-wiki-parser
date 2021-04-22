from crawler.core.filter import FilterAbstract
from crawler.core.types import FunctionUrl


class FilterRemoveDuplicates(FilterAbstract):
    def filter_predicate(self):
        def predicate(source: FunctionUrl):
            for url in self.context.url_list:
                # TODO: Decrease complexity (n^2) somehow
                if url.url == source.url:
                    return False

            return True

        return predicate

    def apply(self):
        filtered = filter(self.filter_predicate(), self.context.url_list)
        self.context.url_list = filtered
