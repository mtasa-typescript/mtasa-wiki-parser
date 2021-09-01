from to_typescript.core.filter import FilterAbstract


class FilterGetDump(FilterAbstract):
    def get_dump(self):
        """
        Gets dumped
        """
        from to_python.dump import DUMP_FUNCTIONS
        from to_python.dump import DUMP_EVENTS
        from to_python.dump import DUMP_OOPS

        self.context.functions = DUMP_FUNCTIONS
        self.context.events = DUMP_EVENTS
        self.context.oops = DUMP_OOPS

    def apply(self):
        self.get_dump()
        print(f'Got all Dumps:  \u001b[34m{len(self.context.functions)}\u001b[0m')