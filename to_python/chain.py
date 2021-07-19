from typing import List

from to_python.core.filter import FilterAbstract
from to_python.filters.collect_files import FilterCollectDumpFiles
from to_python.filters.data_list.doc import FilterParseDocs
from to_python.filters.data_list.init import FilterInitInternalList
from to_python.filters.data_list.oop import FilterParseFunctionOOP
from to_python.filters.data_list.raw_post_process import FilterRawPostProcess
from to_python.filters.data_list.side import FilterParseFunctionSide
from to_python.filters.data_list.signature import FilterParseFunctionSignature
from to_python.filters.data_list.wtp import FilterWikiTextParser
from to_python.filters.get_urls import FilterGetFunctionUrls, FilterGetEventUrls
from to_python.filters.save import FilterSaveData

FILTER_CHAIN: List[FilterAbstract]

FILTER_CHAIN = [
    FilterGetFunctionUrls(),
    FilterCollectDumpFiles('functions'),
    FilterInitInternalList('functions'),
    FilterRawPostProcess('functions'),
    FilterParseFunctionSide(),
    FilterWikiTextParser('functions'),
    FilterParseDocs('functions'),
    FilterParseFunctionSignature(),
    FilterParseFunctionOOP(),
    FilterSaveData(), # TODO:

    FilterGetEventUrls(),
    FilterCollectDumpFiles('events'),
    FilterInitInternalList('events'),
    FilterRawPostProcess('events'),
    # TODO: FilterParseEventSide(),
    FilterWikiTextParser('events'),
    FilterParseDocs('events'),
    # TODO: FilterParseFunctionSignature, FilterParseFunctionOOP, FilterSaveData
]
