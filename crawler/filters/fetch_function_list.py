from typing import List, Optional

import requests
from bs4 import BeautifulSoup, Tag

from crawler.config import HOST_URL
from crawler.core.filter import FilterAbstract
from crawler.core.types import ListType, PageUrl


class FunctionListParseError(RuntimeError):
    pass


class FilterFetchList(FilterAbstract):
    URL_MAP = {
        ListType.CLIENT: f'{HOST_URL}/wiki/Client_Scripting_Functions',
        ListType.SERVER: f'{HOST_URL}/wiki/Server_Scripting_Functions',
    }

    list_type: ListType

    current_item_category: Optional[str] = None

    def __init__(self, list_type: ListType):
        super().__init__(list_type)

        self.list_type = list_type

    def process_list_item(self, tag: Tag) -> Optional[PageUrl]:
        if tag.name != 'h2' and self.current_item_category is None:
            raise FunctionListParseError('First category is not specified')

        if tag.name == 'h2':
            self.current_item_category = tag.text
            return None

        if 'href' in tag.attrs:
            return PageUrl(url=tag.attrs['href'],
                           name=tag.text,
                           category=self.current_item_category,
                           type=self.list_type)

    def download_list_tags(self) -> List[Tag]:
        """
        Download and parse byb BeautifulSoup
        :return: Tag list
        """
        req = requests.request('GET', url=self.URL_MAP[self.list_type])
        html = req.text
        soup_list = BeautifulSoup(html, 'html.parser')
        soup_list.select_one('#toc').extract()  # Remove Table Of Content

        container = soup_list.select_one('#mw-content-text')
        return container.select('ul a, h2')

    def download_list(self) -> List[PageUrl]:
        categorized_links = self.download_list_tags()

        result: List[PageUrl] = [self.process_list_item(tag) for tag in categorized_links]
        result = list(filter(lambda v: v is not None, result))

        return result

    def apply(self):
        result = self.download_list()
        self.context.url_list.extend(result)
        print(f'Downloaded list for {self.list_type}')
