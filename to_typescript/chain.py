from typing import List

from to_typescript.core.filter import FilterAbstract
from to_typescript.filters.event_declarations import FilterEventSaveDeclarations
from to_typescript.filters.event_index import FilterEventSaveIndex
from to_typescript.filters.event_names import FilterEventSaveNames
from to_typescript.filters.function_declarations import FilterGenerateFunctionDeclarations
from to_typescript.filters.function_save import FilterFunctionSave
from to_typescript.filters.function_save_index import FilterFunctionSaveIndex
from to_typescript.filters.get_dump import FilterGetDump
from to_typescript.filters.get_urls import FilterGetUrls
from to_typescript.filters.oop_declarations import FilterGenerateOOPDeclarations
from to_typescript.filters.oop_save import FilterOOPSave
from to_typescript.filters.processing_event import FilterDumpProcessEvents
from to_typescript.filters.processing_function import FilterDumpProcessFunctions
from to_typescript.filters.processing_oop import FilterDumpProcessOOP
from to_typescript.filters.processing_post import FilterDumpProcessPost

FILTER_CHAIN: List[FilterAbstract]

FILTER_CHAIN = [
    FilterGetUrls(),
    FilterGetDump(),

    FilterDumpProcessFunctions(),
    FilterDumpProcessOOP(),
    FilterDumpProcessEvents(),
    FilterDumpProcessPost(),

    FilterGenerateFunctionDeclarations(),
    FilterFunctionSave(),

    FilterGenerateOOPDeclarations(),
    FilterOOPSave(),

    FilterFunctionSaveIndex(),

    FilterEventSaveNames(),
    FilterEventSaveDeclarations(),
    FilterEventSaveIndex(),
]
