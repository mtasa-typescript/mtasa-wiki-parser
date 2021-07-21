from to_typescript.core.filter import FilterAbstract


class FilterGetDump(FilterAbstract):
    def get_dump(self):
        """
        Gets dumped
        """
        from to_python.dump import DUMP_FUNCTIONS
        from to_python.dump import DUMP_EVENTS

        self.context.functions = DUMP_FUNCTIONS
        self.context.events = DUMP_EVENTS

    def apply(self):
        self.get_dump()
        print(f'Got all Dumps: {len(self.context.functions)}')