from typing import List, Any

from crawler.core.filter import FilterAbstract
from crawler.core.types import ListType
from crawler.filters.fetch_functions import FilterFetchFunctions
from crawler.filters.fetch_list import FilterFetchList
from crawler.filters.remove_duplicates import FilterRemoveDuplicates
from crawler.filters.save_fetched import FilterSaveFetched

FILTER_CHAIN: List[FilterAbstract]

FILTER_CHAIN = [
    FilterFetchList(ListType.CLIENT),
    FilterFetchList(ListType.SERVER),
    FilterRemoveDuplicates(),
    FilterFetchFunctions(),
    FilterSaveFetched(),
]