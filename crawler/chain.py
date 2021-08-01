from typing import List

from crawler.core.filter import FilterAbstract, Context
from crawler.core.types import ListType
from crawler.filters.fetch_event_functions import FilterFetchEvents
from crawler.filters.fetch_event_list import FilterFetchEventList
from crawler.filters.fetch_function_list import FilterFetchList
from crawler.filters.fetch_function_pages import FilterFetchFunctions
from crawler.filters.remove_duplicates import FilterRemoveDuplicates
from crawler.filters.save_event_fetched import FilterSaveFetchedEvents
from crawler.filters.save_function_fetched import FilterSaveFetched


def get_filter_chain(context: Context) -> List[FilterAbstract]:
    return [
        FilterFetchList(ListType.CLIENT),
        FilterFetchList(ListType.SERVER),
        FilterRemoveDuplicates(context.url_list),
        FilterFetchFunctions(),
        FilterSaveFetched(),
    ]


def get_event_filter_chain(context: Context) -> List[FilterAbstract]:
    return [
        FilterFetchEventList(ListType.CLIENT),
        FilterFetchEventList(ListType.SERVER),
        FilterRemoveDuplicates(context.event_url_list),
        FilterFetchEvents(),
        FilterSaveFetchedEvents(),
    ]
