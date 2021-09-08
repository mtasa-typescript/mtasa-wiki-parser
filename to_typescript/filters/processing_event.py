from typing import List

from to_python.core.types import EventData
from to_typescript.core.filter import FilterAbstract
from to_typescript.filters.processing_function import \
    FilterDumpProcessFunctions


class FilterDumpProcessEvents(FilterAbstract):
    """
    Post processing for events.
    Fills self.context.events_declarations
    < category , < client/server, [event data] > >
    """

    def prepare_event(self,
                      data_list_index: int,
                      data_list: List[EventData]) -> int:
        """
        Calls preparation method for the passed function.
        :return: New index in List[FunctionData]
        """
        increment = 1

        data = data_list[data_list_index]
        FilterDumpProcessFunctions.prepare_argument_names(
            data.arguments.arguments)
        FilterDumpProcessFunctions.prepare_argument_types(
            data.arguments.arguments)

        increment = +1

        return data_list_index + increment

    def apply(self):
        for event in self.context.events:
            for side, data in event:
                category = self.context.urls[data[0].name].category
                self.context.events_declarations[category][side].append(data)

                self.prepare_event(data_list_index=0,
                                   data_list=data)

        print('\u001b[32mEvents processing complete\u001b[0m')
