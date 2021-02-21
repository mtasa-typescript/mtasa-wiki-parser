from typing import List

import requests
from bs4 import BeautifulSoup, Tag

from src.fetch.function import ListType, FunctionUrl
from src.fetch.globals import HOST_URL

URL_MAP = {
    ListType.CLIENT: f'{HOST_URL}/wiki/Client_Scripting_Functions',
    ListType.SERVER: f'{HOST_URL}/wiki/Server_Scripting_Functions',
}


class FunctionListParseError(RuntimeError):
    pass


class FunctionListParseNoFirstCategoryError(RuntimeError):
    pass


def get_function_list(list_type: ListType) -> List[FunctionUrl]:
    req = requests.request('GET', url=URL_MAP[list_type])
    html = req.text
    soup_list = BeautifulSoup(html, 'html.parser')
    soup_list.select_one('#toc').extract()  # Remove Table Of Content

    container = soup_list.select_one('#mw-content-text')
    categorized_links: List[Tag] = container.select('ul a, h2')

    result: List[FunctionUrl] = []
    category = None
    for element in categorized_links:
        if element.name != 'h2' and category is None:
            raise FunctionListParseNoFirstCategoryError()

        if element.name == 'h2':
            category = element.text
            continue

        if 'href' in element.attrs:
            if [url for url in result if url.name == element.text]:
                continue  # Function already exists

            result.append(FunctionUrl(url=element.attrs['href'],
                                      name=element.text,
                                      category=category,
                                      function_type=list_type))

    return result
