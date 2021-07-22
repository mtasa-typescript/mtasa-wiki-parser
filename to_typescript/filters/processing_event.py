from to_typescript.core.filter import FilterAbstract


class FilterDumpProcessEvents(FilterAbstract):
    """
    Post processing for events.
    Fills self.context.events_declarations
    < category , < client/server, [event data] > >
    """

    def apply(self):
        for event in self.context.events:
            for side, data in event:
                category = self.context.urls[data[0].name].category
                self.context.events_declarations[category][side].append(data)
