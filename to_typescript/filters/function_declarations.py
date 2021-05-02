from typing import Dict

from crawler.core.types import FunctionUrl
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

    def generate_declaration(self, compound: CompoundFunctionData, url: FunctionUrl):
        sides: Dict[str, FunctionData] = dict()
        if compound.server:
            sides['server'] = compound.server
        if compound.client:
            sides['client'] = compound.client

        for side in sides:
            data = sides[side]
            declaration = TypeScriptFunctionGenerator(host_name=self.context.host_name,
                                                      data=data,
                                                      url=url).generate()

            category = self.get_dts_file_name(url.category)
            self.context.declarations.function[category][side].append(declaration)

    def apply(self):
        for function in self.context.functions:
            name = (function.server or function.client).name
            self.generate_declaration(function, self.context.urls[name])

        print('Declarations generated')
