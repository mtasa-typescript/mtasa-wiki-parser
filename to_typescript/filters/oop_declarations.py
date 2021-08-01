from collections import defaultdict
from typing import Set, DefaultDict

from crawler.core.types import PageUrl
from to_python.core.types import CompoundFunctionData
from to_typescript.core.filter import FilterAbstract
from to_typescript.core.transform.function import TypeScriptFunctionGenerator
from to_typescript.core.transform.oop import TypeScriptOOPGenerator


class FilterGenerateOOPDeclarations(FilterAbstract):
    def __init__(self):
        super().__init__()

        # < function name, <side, prop list> >
        self.fields_in_class: DefaultDict[str, DefaultDict[str, Set[str]]] = defaultdict(lambda: defaultdict(set))

    def generate_declaration(self, compound: CompoundFunctionData, url: PageUrl):
        for side, data_list in compound:
            for data in data_list:
                if data.oop is None:
                    continue

                file_name = data.oop.class_name
                field_name = data.oop.field

                declaration_field = TypeScriptOOPGenerator(host_name=self.context.host_name,
                                                           data=data,
                                                           url=url).generate_field()
                declaration_method = TypeScriptOOPGenerator(host_name=self.context.host_name,
                                                            data=data,
                                                            url=url).generate_method()

                if declaration_field and field_name not in self.fields_in_class[file_name][side]:
                    self.fields_in_class[file_name][side].add(field_name)

                    self.context.declarations.oop_fields[file_name][side].append(declaration_field)

                if declaration_method:
                    self.context.declarations.oop_methods[file_name][side].append(declaration_method)

                    # Adds class generic (template) string
                    if data.oop.method_name == 'constructor':
                        self.context.declarations.oop_class_templates[file_name][side].append(
                            TypeScriptFunctionGenerator.generate_generics(data.signature.generic_types)
                        )

    def apply(self):
        """
        Generates OOP declarations
        """
        for function in self.context.functions:
            name = (function.server or function.client)[0].name
            url = self.context.urls[name]
            self.generate_declaration(function, url)

        print('OOP Declarations generated\u001b[0m')
