import abc
from typing import Union

from to_python.core.context import Context, ContextData
from to_python.core.types import CompoundFunctionData, CompoundEventData


class FilterAbstract(metaclass=abc.ABCMeta):
    context: Context
    context_data: ContextData

    def __init__(self, context_type: str):
        """
        :param context_type: `functions` or `events`
        """
        self.context_type = context_type

    def initialize(self, context: Context):
        """
        Initialize in runtime
        :param context: Global context
        """
        self.context = context
        self.context_data: ContextData[Union[CompoundFunctionData, CompoundEventData]] = \
            getattr(context, self.context_type)

    @abc.abstractmethod
    def apply(self):
        """
        Applies filter
        """
        pass
