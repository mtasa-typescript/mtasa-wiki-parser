import abc
import enum
from dataclasses import dataclass, field
from typing import Optional, Tuple, Any, Dict

from wikitextparser import WikiText

from crawler.core.types import PageUrl
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
class ContextData:
    """
    Context about set of pages
    """

    # Contains <function name, file path>
    pages: Dict[str, str] = field(default_factory=dict)

    # Parsed functions
    parsed: Dict[str, CompoundFunctionData] = field(default_factory=dict)

    # Raw data <function name, data>
    raw_data: Dict[str, str] = field(default_factory=dict)

    # Side data <function name, side data>
    side_data: Dict[str, RawSide] = field(default_factory=dict)

    # Raw data parsed by wtp
    wiki_raw: Dict[str, WikiText] = field(default_factory=dict)

    # Side data parsed by wtp
    wiki_side: Dict[str, WikiSide] = field(default_factory=dict)

    # URLs from URL List
    urls: Dict[str, PageUrl] = field(default_factory=dict)


@dataclass
class Context:
    """
    Context with functions and events data
    """

    functions: ContextData
    events: ContextData
