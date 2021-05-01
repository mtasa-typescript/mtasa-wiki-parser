import abc
import enum
from dataclasses import dataclass
from typing import Optional, Tuple, Any, Dict

from wikitextparser import WikiText

from crawler.core.types import FunctionUrl
from to_python.core.types import CompoundFunctionData


class ParseFunctionSide(enum.Enum):
    CLIENT = 'Client'
    SERVER = 'Server'
    SHARED = 'Shared'


class IterableSide(metaclass=abc.ABCMeta):
    server: Any
    client: Any

    def __iter__(self) -> Tuple[str, str]:
        if self.server is not None:
            yield 'server', self.server
        if self.client is not None:
            yield 'client', self.client


@dataclass
class RawSide(IterableSide):
    side: ParseFunctionSide
    server: Optional[str]
    client: Optional[str]


@dataclass
class WikiSide(IterableSide):
    side: ParseFunctionSide
    server: Optional[WikiText]
    client: Optional[WikiText]


@dataclass
class Context:
    # Contains <function name, file path>
    functions: Dict[str, str]

    # Parsed functions
    parsed: Dict[str, CompoundFunctionData]

    # Raw data <function name, data>
    raw_data: Dict[str, str]

    # Side data <function name, side data>
    side_data: Dict[str, RawSide]

    # Raw data parsed by wtp
    wiki_raw: Dict[str, WikiText]

    # Side data parsed by wtp
    wiki_side: Dict[str, WikiSide]

    # URLs from URL List
    urls: Dict[str, FunctionUrl]
