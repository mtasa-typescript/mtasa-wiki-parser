from typing import List

from crawler.core.types import ListType
from to_python.core.filter import FilterAbstract
from to_python.filters.collect_files import FilterCollectDumpFiles
from to_python.filters.data_list.init import FilterInitInternalList
from to_python.filters.data_list.raw_post_process import FilterRawPostProcess
from to_python.filters.data_list.side import FilterParseSide
from to_python.filters.data_list.wtp_sample import FilterWikiTextParser

FILTER_CHAIN: List[FilterAbstract]

FILTER_CHAIN = [
    FilterCollectDumpFiles(),
    FilterInitInternalList(),
    FilterRawPostProcess(),
    FilterParseSide(),
    FilterWikiTextParser(),
]
