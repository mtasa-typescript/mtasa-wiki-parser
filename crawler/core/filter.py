import abc
from dataclasses import dataclass, field
from typing import Optional, List, Tuple, Set

from crawler.core.types import ListType, PageUrl


@dataclass
class Context:
    host_url: str
    fetch_batch_size: int

    function_subfolder: str
    fetch_start_from: Optional[Tuple[ListType, str]]
    blacklist: Set[str]

    event_subfolder: str
    event_fetch_start_from: Optional[Tuple[ListType, str]]
    event_blacklist: Set[str]

    url_list: List[PageUrl] = field(default_factory=list)
    fetched: List[Tuple[PageUrl, str]] = field(default_factory=list)

    event_url_list: List[PageUrl] = field(default_factory=list)
    event_fetched: List[Tuple[PageUrl, str]] = field(default_factory=list)


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
