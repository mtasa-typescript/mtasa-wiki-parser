from to_typescript.core.filter import FilterAbstract


class FilterSortFunctionDeclarations(FilterAbstract):
    def apply(self):
        for key in self.context.declarations.function:
            function = self.context.declarations.function[key]
            for side in function:
                function[side] = sorted(function[side])

        print('Function Declarations sorted\u001b[0m')
