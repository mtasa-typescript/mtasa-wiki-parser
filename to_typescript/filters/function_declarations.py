from typing import Dict, List

from crawler.core.types import PageUrl
from to_python.core.types import CompoundFunctionData, FunctionData
from to_typescript.core.filter import FilterAbstract
from to_typescript.core.transform.function import TypeScriptFunctionGenerator


class FilterGenerateFunctionDeclarations(FilterAbstract):
    @staticmethod
    def get_dts_file_name(category: str) -> str:
        """
        Converts category into .d.ts filename
        """
        return (category
                .strip()
                .split(' ')[0]
                .lower())

    def generate_declaration(self, compound: CompoundFunctionData, url: PageUrl):
        # TODO: use CompoundFunctionData __iter__ (loop)

        sides: Dict[str, List[FunctionData]] = dict()
        if compound.server:
            sides['server'] = compound.server
        if compound.client:
            sides['client'] = compound.client

        for side in sides:
            for data in sides[side]:
                declaration = TypeScriptFunctionGenerator(host_name=self.context.host_name,
                                                          data=data,
                                                          url=url).generate()

                category = self.get_dts_file_name(url.category)
                self.context.declarations.function[category][side].append(declaration)

    def save_function_for_index(self, compound: CompoundFunctionData, url: PageUrl):
        """
        Generates self.context.declarations.function_names
        """
        category = self.get_dts_file_name(url.category)

        for side, data in compound:
            self.context.declarations.function_names[category][side].append(url.name)

    def apply(self):
        for function in self.context.functions:
            name = (function.server or function.client)[0].url
            url = self.context.urls[name]
            self.generate_declaration(function, url)

            self.save_function_for_index(function, url)

        print('Function Declarations generated\u001b[0m')
