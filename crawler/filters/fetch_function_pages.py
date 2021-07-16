from typing import List, Dict, Any, Tuple, Generator, Collection, Optional

import requests

from crawler.core.filter import FilterAbstract
from crawler.core.types import PageUrl, ListType


class WikiPageFetchError(RuntimeError):
    pass


class WikiPageFetcher():
    """
    Fetches MTASA Wiki pages
    """

    def __init__(self, pages: List[str], host: str, batch_size=16):
        """
        :param pages: URL list
        :param host: Host URL
        :param batch_size: Amount of pages will be received per one request
        """
        self.pages = pages
        self.host = host
        self.batch_size = batch_size

    @staticmethod
    def normalize_page_name(name: str) -> str:
        return name[0].upper() + name[1:]

    def fetch_batch(self, batch: List[str]) -> Dict[str, str]:
        """
        Fetches a batch of the urls
        :return: Dictionary: Key is the URL, value is the content of the page
        """
        query_titles = '|'.join(batch)
        url = f'{self.host}/api.php?' \
              f'action=query&' \
              f'prop=revisions&' \
              f'titles={query_titles}&' \
              f'rvslots=*&' \
              f'rvprop=content&' \
              f'format=json'

        req = requests.request('GET', url)
        data = req.json()
        query = data['query']
        pages = query['pages']

        result = dict()
        for key in pages:
            page: dict = pages[key]
            if 'missing' in page:
                raise WikiPageFetchError(f'Page "{page["title"]}" not found')

            revisions = page["revisions"]
            slots = revisions[0]["slots"]
            main_slot = slots["main"]
            content = main_slot["*"]

            result[page["title"]] = content + '\n'

        return result

    def fetch(self) -> Generator[Tuple[str, str], Any, None]:
        """
        Fetches all passed pages
        """
        batches = [self.pages[x:x + self.batch_size] for x in range(0, len(self.pages), self.batch_size)]
        for batch in batches:
            result = self.fetch_batch(batch)

            for key in result:
                yield key, result[key]


class FilterFetchFunctionsError(RuntimeError):
    pass


class FilterFetchFunctions(FilterAbstract):
    """
    Fetches functions defined in the URL List
    """

    def generate_url_list_dict(self,
                               url_list: List[PageUrl],
                               start_from: Optional[Tuple[ListType, str]],
                               blacklist: Collection[str]) -> Dict[str, PageUrl]:
        """
        Generates dictionary with URLs
        :return: Dictionary. Key is the name (string), value is the PageUrl
        """
        enable_fetch = False
        if start_from is None:
            print('All pages will be cached')
            enable_fetch = True
        else:
            print(f'Pages will begin to be cached from the "{start_from[1]}", "{start_from[0]}"')

        result = dict()

        for j, url in enumerate(url_list):
            if url.name in blacklist:
                print(f'Blacklisted {url.name}')
                continue

            if not enable_fetch and url.name == start_from[1] and url.type == start_from[0]:
                enable_fetch = True
            if not enable_fetch:
                print(f'Skipped "{url.name}", {url.type.name}')
                continue

            result[WikiPageFetcher.normalize_page_name(url.name)] = url

        return result

    def apply(self):
        print('Functions fetch began')

        url_dict = self.generate_url_list_dict(url_list=self.context.url_list,
                                               blacklist=self.context.blacklist,
                                               start_from=self.context.fetch_start_from, )
        keys = list(url_dict.keys())

        counter = 0
        for name, content in WikiPageFetcher(keys, self.context.host_url, self.context.fetch_batch_size).fetch():
            if name not in url_dict:
                raise FilterFetchFunctionsError(f'Not found key {name} in url_dict. Have you normalized the URL names?')

            url_object = url_dict[name]
            counter += 1

            print(f'Fetched [{counter}/{len(url_dict)}] "{url_object.name}", {url_object.type.name}')

            self.context.fetched.append((url_dict[name], content))
