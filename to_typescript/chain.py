from typing import List

from to_python.core.filter import FilterAbstract
from to_typescript.filters.function_save_index import FilterFunctionSaveIndex
from to_typescript.filters.processing import FilterDumpProcess
from to_typescript.filters.function_declarations import FilterGenerateFunctionDeclarations
from to_typescript.filters.function_save import FilterFunctionSave
from to_typescript.filters.get_dump import FilterGetDump
from to_typescript.filters.get_urls import FilterGetUrls

FILTER_CHAIN: List[FilterAbstract]

FILTER_CHAIN = [
    FilterGetUrls(),
    FilterGetDump(),
    FilterDumpProcess(),
    FilterGenerateFunctionDeclarations(),
    FilterFunctionSave(),
    FilterFunctionSaveIndex(),
]
