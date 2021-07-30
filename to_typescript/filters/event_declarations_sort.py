from to_typescript.core.filter import FilterAbstract


class FilterSortOOPDeclarations(FilterAbstract):
    def apply(self):
        for key in self.context.declarations.oop_methods:
            function = self.context.declarations.oop_methods[key]
            for side in function:
                function[side] = sorted(function[side])

        for key in self.context.declarations.oop_fields:
            function = self.context.declarations.oop_fields[key]
            for side in function:
                function[side] = sorted(function[side])

        print('Function OOP fields and methods sorted')
