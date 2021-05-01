from dataclasses import dataclass
from typing import Dict, List

from crawler.core.types import FunctionUrl
from to_python.core.types import CompoundFunctionData


@dataclass
class Context:
    # Functions from to_python dump repository
    functions: List[CompoundFunctionData]

    # URLs from URL List
    urls: Dict[str, FunctionUrl]
