import os
from typing import List

from crawler.core.types import PageUrl
from crawler.filters.save_function_fetched import FilterSaveFetched


class FilterSaveFetchedEvents(FilterSaveFetched):
    @staticmethod
    def text_event_url_list(url_list: List[PageUrl]) -> str:
        """
        Converts URL List into a text
        """
        text = '\n\n' \
               'EVENT_URL_LIST = [\n    ' + ',\n    '.join(repr(v) for v in url_list) + '\n]\n'

        return text

    def save_event_url_list(self):
        """
        Saves fetched url list
        """
        cache_file = os.path.join(self.DUMP_FOLDER, '__init__.py')

        with open(cache_file, 'a', encoding='UTF-8', newline='\n') as cache:
            cache.write(self.text_event_url_list(self.context.event_url_list))

    def apply(self):
        for url, text in self.context.event_fetched:
            self.save_file(url, text, url.name[2:4].upper())
            print(f'Saved "{url.name}", {url.type.name}')

        self.save_event_url_list()
        print(f'Saved URL List')
