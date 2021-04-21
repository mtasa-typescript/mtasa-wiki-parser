import abc
from dataclasses import dataclass
from typing import Optional, Any, Dict, List

from crawler.core.types import ListType, FunctionUrl


@dataclass
class Context:
    host_url: str
    fetch_start_from: Optional[ListType, str]
    data: Dict[str, Any]
    url_list: List[FunctionUrl]


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
