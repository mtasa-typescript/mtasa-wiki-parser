import abc
import enum
from dataclasses import dataclass
from typing import Any, Dict, Optional

from to_python.core.types import CompoundFunctionData


class ParseFunctionSide(enum.Enum):
    CLIENT = 'Client'
    SERVER = 'Server'
    SHARED = 'Shared'


@dataclass
class RawSide:
    side: ParseFunctionSide
    server: Optional[str]
    client: Optional[str]


@dataclass
class Context:
    # Contains <function name, file path>
    functions: Dict[str, str]

    # Contains parsed functions
    parsed: Dict[str, CompoundFunctionData]

    # Contains raw data
    raw_data: Dict[str, str]

    # Contains side data
    side_data: Dict[str, RawSide]

    data: Dict[str, Any]


class FilterAbstract(metaclass=abc.ABCMeta):
    context: Context

    def initialize(self, context: Context):
        """
        Initialize in runtime
        :param context: Global context
        """
        self.context = context

    @abc.abstractmethod
    def apply(self):
        """
        Applies filter
        """
        pass
