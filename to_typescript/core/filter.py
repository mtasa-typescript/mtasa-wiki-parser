import abc

from to_typescript.core.context import Context


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
