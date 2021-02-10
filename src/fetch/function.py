# Source: MediaWiki
import enum
from dataclasses import dataclass
from typing import List, Dict, Optional

import requests
from bs4 import BeautifulSoup

from src.fetch.globals import HOST_URL


class ListType(enum.Enum):
    CLIENT = 'Client'
    SERVER = 'Server'

    def __repr__(self) -> str:
        if self == self.CLIENT:
            return 'ListType.CLIENT'
        if self == self.SERVER:
            return 'ListType.SERVER'


@dataclass
class FunctionUrl:
    url: str
    name: str
    category: str
    function_type: ListType

    def get_full_url(self) -> str:
        return f'{HOST_URL}{self.url}'


@dataclass
class FunctionArgument:
    name: str
    argument_type: str
    default_value: Optional[str]
    optional: bool


@dataclass
class FunctionType:
    """
    Function information (default style)
    """
    name: str
    return_types: List[str]
    arguments: List[FunctionArgument]


@dataclass
class FunctionDoc:
    """
    Docs for function
    """
    description: str
    arguments: Dict[str, str]
    result: str


@dataclass
class FunctionOOP:
    """
    Function OOP information
    """
    class_name: str
    method_name: str
    field: Optional[str]


@dataclass
class FunctionData:
    """
    All function data from wiki
    """
    signature: FunctionType
    docs: FunctionDoc
    oop: Optional[FunctionOOP]
    url: FunctionUrl


@dataclass
class CompoundFunctionData:
    server: Optional[FunctionData] = None
    client: Optional[FunctionData] = None
