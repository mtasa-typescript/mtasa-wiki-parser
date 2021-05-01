from typing import List

from to_python.core.filter import FilterAbstract
from to_typescript.filters.get_dump import FilterGetDump
from to_typescript.filters.get_urls import FilterGetUrls

FILTER_CHAIN: List[FilterAbstract]

FILTER_CHAIN = [
    FilterGetUrls(),
    FilterGetDump(),
]
