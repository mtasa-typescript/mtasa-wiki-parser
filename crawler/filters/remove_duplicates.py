from crawler.core.filter import FilterAbstract
from crawler.core.types import FunctionUrl


class FilterRemoveDuplicates(FilterAbstract):
    def filter_predicate(self):
        url_list = self.context.url_list

        def predicate(source: FunctionUrl):
            for i in range(url_list.index(source)+1, len(url_list)):
                url = url_list[i]
                # TODO: Decrease complexity (n^2) somehow
                if url.url == source.url:
                    return False

            return True

        return predicate

    def apply(self):
        filtered = filter(self.filter_predicate(), self.context.url_list)
        self.context.url_list = list(filtered)
