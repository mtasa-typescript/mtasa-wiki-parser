from typing import List

from crawler.core.filter import FilterAbstract
from crawler.core.types import PageUrl


class FilterRemoveDuplicates(FilterAbstract):
    def __init__(self, url_list: List):
        super().__init__()

        self.url_list = url_list

    def filter_predicate(self):
        def predicate(source: PageUrl):
            for i in range(self.url_list.index(source) + 1,
                           len(self.url_list)):

                url = self.url_list[i]
                # TODO: Decrease complexity (n^2) somehow
                if url.url == source.url:
                    return False

            return True

        return predicate

    def apply(self):
        filtered = filter(self.filter_predicate(), self.url_list)

        # Replace from the origin
        self.url_list[:] = list(filtered)
