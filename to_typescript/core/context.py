from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, DefaultDict

from crawler.core.types import FunctionUrl
from to_python.core.types import CompoundFunctionData

# <category, <client/server, <declaration>>>
DictType = DefaultDict[str, DefaultDict[str, List[str]]]


def default_dict_factory():
    return defaultdict(lambda: defaultdict(list))


@dataclass
class ContextDeclarations:
    # <category, <client/server, <declaration>>>
    DictType = DefaultDict[str, DefaultDict[str, List[str]]]

    function: 'ContextDeclarations.DictType' = field(default_factory=default_dict_factory)
    oop: 'ContextDeclarations.DictType' = field(default_factory=default_dict_factory)

    # Just names for index.d.ts file
    # <category, <client/server, [function name]>>
    function_names: 'ContextDeclarations.DictType' = field(default_factory=default_dict_factory)


@dataclass
class Context:
    # MTASA Wiki host instance
    host_name: str

    # Functions from to_python dump repository
    functions: List[CompoundFunctionData] = field(default_factory=list)

    # URLs from URL List
    urls: Dict[str, FunctionUrl] = field(default_factory=dict)

    # Generated declarations
    declarations: ContextDeclarations = field(default_factory=ContextDeclarations)
