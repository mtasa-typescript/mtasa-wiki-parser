# Source: MediaWiki
import enum
from dataclasses import dataclass
from typing import List, Dict, Optional

from globals import HOST_URL


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
