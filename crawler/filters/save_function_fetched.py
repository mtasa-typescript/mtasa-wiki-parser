import os
from typing import List, Optional

from crawler.core.filter import FilterAbstract
from crawler.core.types import PageUrl
from crawler.filters.fetch_function_pages import WikiPageFetcher


class FilterSaveFetched(FilterAbstract):
    DUMP_FOLDER = 'dump_html'

    def save_file(self, url: PageUrl, result: str, subdir: Optional[str] = None):
        """
        Saves fetched data into a file
        :param url: Data about the function
        :param result: Fetched data
        :param subdir: Subdirectory with data (relative path, based on DUMP folder)
        """
        name = WikiPageFetcher.normalize_page_name(url.name)
        if subdir is None:
            subdir = os.path.join(self.DUMP_FOLDER, name[:2].upper())
        else:
            subdir = os.path.join(self.DUMP_FOLDER, subdir)

        cache_file = os.path.join(subdir, name)

        if not os.path.exists(self.DUMP_FOLDER):
            os.mkdir(self.DUMP_FOLDER)
        if not os.path.exists(subdir):
            os.mkdir(subdir)

        with open(cache_file, 'w', encoding='UTF-8', newline='\n') as cache:
            cache.write(result)

    @staticmethod
    def text_url_list(url_list: List[PageUrl], variable_name: str = 'URL_LIST') -> str:
        """
        Converts URL List into a text
        """
        text = 'from crawler.core.types import PageUrl, ListType\n\n'
        text += f'{variable_name} = [\n    ' + ',\n    '.join(repr(v) for v in url_list) + '\n]\n'

        return text

    def save_url_list(self):
        """
        Saves fetched url list
        """
        cache_file = os.path.join(self.DUMP_FOLDER, '__init__.py')

        with open(cache_file, 'w', encoding='UTF-8', newline='\n') as cache:
            cache.write(self.text_url_list(self.context.url_list))

    def apply(self):
        for url, text in self.context.fetched:
            self.save_file(
                url,
                text,
                os.path.join(self.context.function_subfolder, url.name[:2].upper())
            )
            print(f'Saved "{url.name}", {url.type.name}')

        self.save_url_list()
        print(f'Saved URL List')
