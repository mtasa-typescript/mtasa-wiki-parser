import os
from typing import List

from crawler.core.filter import FilterAbstract
from crawler.core.types import FunctionUrl
from crawler.filters.fetch_functions import FilterFetchFunctions


class FilterSaveFetched(FilterAbstract):
    DUMP_FOLDER = 'dump_html'

    def save_file(self, url: FunctionUrl, result: str):
        """
        Saves fetched data into a file
        :param url: Data about the function
        :param result: Fetched data
        """
        name = FilterFetchFunctions.get_function_name(url)
        subfolder = os.path.join(self.DUMP_FOLDER, name[:2].upper())
        cache_file = os.path.join(subfolder, name)

        if not os.path.exists(self.DUMP_FOLDER):
            os.mkdir(self.DUMP_FOLDER)
        if not os.path.exists(subfolder):
            os.mkdir(subfolder)

        with open(cache_file, 'w', encoding='UTF-8') as cache:
            cache.write(result)

    @staticmethod
    def text_url_list(url_list: List[FunctionUrl]) -> str:
        """
        Converts URL List into a text
        """
        text = 'from crawler.core.types import FunctionUrl, ListType\n\n'
        text += 'URL_LIST = [\n    ' + ',\n    '.join(repr(v) for v in url_list) + '\n]\n'

        return text

    def save_url_list(self):
        """
        Saves fetched url list
        """
        cache_file = os.path.join(self.DUMP_FOLDER, '__init__.py')

        with open(cache_file, 'w', encoding='UTF-8') as cache:
            cache.write(self.text_url_list(self.context.url_list))

    def apply(self):
        for url, text in self.context.fetched:
            self.save_file(url, text)
            print(f'Saved "{url.name}", {url.function_type.name}')

        self.save_url_list()
        print(f'Saved URL List')
