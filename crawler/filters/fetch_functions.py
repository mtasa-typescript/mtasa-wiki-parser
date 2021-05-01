import sys
import traceback

import requests
from bs4 import BeautifulSoup

from crawler.core.filter import FilterAbstract
from crawler.core.types import FunctionUrl


class FunctionFetchError(RuntimeError):
    pass


class FilterFetchFunctions(FilterAbstract):
    """
    Fetches functions defined in the URL List
    """

    @staticmethod
    def get_function_name(url: FunctionUrl) -> str:
        return url.name[0].upper() + url.name[1:]

    def fetch_function(self, url: FunctionUrl) -> str:
        """
        Fetches page from wiki
        :param url: Data about the function
        :return: Fetched data
        """
        name = self.get_function_name(url)
        urlpath = f'{self.context.host_url}/index.php?title={name}&action=edit'
        req = requests.request('GET', urlpath)
        html = req.text

        soup_wiki = BeautifulSoup(html, 'html.parser')
        source_field = soup_wiki.select_one('#wpTextbox1')

        return source_field.contents[0]

    def apply(self):
        enable_fetch = False
        start_from = self.context.fetch_start_from
        if self.context.fetch_start_from is None:
            print('All functions will be cached')
            enable_fetch = True
        else:
            print(f'Functions will be cached from the "{start_from[1]}", "{start_from[0]}"')

        for j, url in enumerate(self.context.url_list):
            if url.name in self.context.blacklist:
                print(f'Blacklisted {url.name}')
                continue

            if not enable_fetch and url.name == start_from[1] and url.function_type == start_from[0]:
                enable_fetch = True
            if not enable_fetch:
                print(f'Skipped "{url.name}", {url.function_type.name}')
                continue

            result = None
            for i in range(3):
                try:
                    result = self.fetch_function(url)
                    print(f'Fetched [{j}/{len(self.context.url_list)}] "{url.name}", {url.function_type.name}')
                    break
                except Exception as e:
                    print('Exception: ', file=sys.stderr)
                    traceback.print_last(file=sys.stderr)
                    print(f'Attempt: {i + 1}', file=sys.stderr)

            if result is None:
                print(f'No result for "{url.name}", {url.function_type.name}.\nEmergency exit...', file=sys.stderr)
                return

            self.context.fetched.append((url, result))
