from to_typescript.core.filter import FilterAbstract


class FilterGetDump(FilterAbstract):
    def get_dump(self):
        """
        Gets dumped
        """
        from to_python.dump import DUMP

        self.context.functions = DUMP

    def apply(self):
        pass