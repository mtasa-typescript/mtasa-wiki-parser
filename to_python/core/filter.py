import abc
import enum
from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple

from wikitextparser import WikiText

from to_python.core.context import Context
from to_python.core.types import CompoundFunctionData


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
