from typing import List

from crawler.core.types import ListType
from to_python.core.filter import FilterAbstract
from to_python.filters.collect_files import FilterCollectDumpFiles
from to_python.filters.data_list.doc import FilterParseDocs
from to_python.filters.data_list.init import FilterInitInternalList
from to_python.filters.data_list.oop import FilterParseFunctionOOP
from to_python.filters.data_list.raw_post_process import FilterRawPostProcess
from to_python.filters.data_list.side import FilterParseSide
from to_python.filters.data_list.signature import FilterParseFunctionSignature
from to_python.filters.data_list.wtp import FilterWikiTextParser
from to_python.filters.save import FilterSaveData

FILTER_CHAIN: List[FilterAbstract]

FILTER_CHAIN = [
    FilterCollectDumpFiles(),
    FilterInitInternalList(),
    FilterRawPostProcess(),
    FilterParseSide(),
    FilterWikiTextParser(),
    FilterParseDocs(),
    FilterParseFunctionSignature(),
    FilterParseFunctionOOP(),
    FilterSaveData(),
]
