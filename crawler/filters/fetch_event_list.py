from typing import List, Optional

from bs4 import Tag

from crawler.config import HOST_URL
from crawler.core.types import ListType, PageUrl
from crawler.filters.fetch_function_list import FilterFetchList


class FunctionListParseError(RuntimeError):
    pass


class FilterFetchEventList(FilterFetchList):
    URL_MAP = {
        ListType.CLIENT: f'{HOST_URL}/wiki/Client_Scripting_Events',
        ListType.SERVER: f'{HOST_URL}/wiki/Server_Scripting_Events',
    }

    list_type: ListType

    current_item_category: Optional[str] = None

    def __init__(self, list_type: ListType):
        super().__init__(list_type)

        self.list_type = list_type

    def process_list_item(self, tag: Tag) -> Optional[PageUrl]:
        super().process_list_item(tag)

        if 'href' in tag.attrs:
            return PageUrl(url=tag.attrs['href'],
                           name=tag.text,
                           category=self.current_item_category,
                           type=self.list_type)

    def download_list(self) -> List[PageUrl]:
        categorized_links = self.download_list_tags()

        result: List[PageUrl] = [self.process_list_item(tag) for tag in
                                 categorized_links]
        result = list(filter(lambda v: v is not None, result))

        return result

    def apply(self):
        result = self.download_list()
        self.context.event_url_list.extend(result)
        print(f'Downloaded event list for {self.list_type}')
