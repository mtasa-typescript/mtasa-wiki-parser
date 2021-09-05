from collections import defaultdict
from typing import Set, DefaultDict, List

from crawler.core.types import PageUrl
from to_python.core.types import FunctionOOP
from to_typescript.core.filter import FilterAbstract
from to_typescript.core.transform.function import TypeScriptFunctionGenerator
from to_typescript.core.transform.oop import TypeScriptOOPGenerator


class FilterGenerateOOPDeclarations(FilterAbstract):
    def __init__(self):
        super().__init__()

        # < function name, <side, prop list> >
        self.fields_in_class: DefaultDict[
            str, DefaultDict[str, Set[str]]] = defaultdict(
            lambda: defaultdict(set))

    def generate_declaration(self,
                             side: str,
                             oop_data: FunctionOOP,
                             url: PageUrl):
        file_name = oop_data.class_name
        field_name = oop_data.field.name if oop_data.field else None

        generator = TypeScriptOOPGenerator(host_name=self.context.host_name,
                                           data=oop_data,
                                           url=url)
        declaration_field = generator.generate_field()
        declaration_method = generator.generate_method()

        if declaration_field and field_name not in \
                self.fields_in_class[file_name][side]:
            self.fields_in_class[file_name][side].add(field_name)

            self.context.declarations.oop_fields[file_name][side].append(
                declaration_field)

        if declaration_method:
            self.context.declarations.oop_methods[file_name][side].append(
                declaration_method)

            # Adds class generic (template) string
            if oop_data.method.name == 'constructor':
                self.context.declarations.oop_class_templates[file_name][
                    side].append(
                    TypeScriptFunctionGenerator.generate_generics(
                        oop_data.method.signature.generic_types)
                )

    def apply(self):
        """
        Generates OOP declarations
        """
        for oop in self.context.oops:
            for side, oop_list in oop:
                oop_list: List[FunctionOOP]

                for oop_data in oop_list:
                    url = self.context.urls[oop_data.method.url]
                    self.generate_declaration(side=side,
                                              oop_data=oop_data,
                                              url=url)

        print('OOP Declarations generated\u001b[0m')
