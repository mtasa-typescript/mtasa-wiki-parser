import re
from copy import deepcopy
from typing import Optional, List

from wikitextparser import WikiText

from to_python.core.filter import FilterAbstract
from to_python.core.format import colorize_oop_token_list
from to_python.core.oop import OOPTokenizer, OOPParser
from to_python.core.types import FunctionOOP, CompoundOOPData, FunctionData, \
    FunctionReturnTypes, \
    FunctionOOPField
from to_python.filters.data_list.signature import WikiGetSyntaxSection


class FilterParseFunctionOOP(FilterAbstract):
    OOP_REGEX = re.compile(r'(\{\{OOP.*\}\})', re.IGNORECASE)

    def __init__(self):
        super().__init__('functions')

    @staticmethod
    def prepare_oop_method(oop_metadata: OOPParser.OutputData,
                           method: FunctionData) -> Optional[FunctionData]:
        method_name = oop_metadata.method_data.method_name
        if method_name is None:
            return None

        method = deepcopy(method)
        method.signature.name = method_name

        return method

    @staticmethod
    def prepare_oop_field(oop_metadata: OOPParser.OutputData,
                          return_types: FunctionReturnTypes) -> \
            Optional[FunctionOOPField]:
        field_name = oop_metadata.field_name
        if field_name is None:
            return None

        return FunctionOOPField(
            name=field_name,
            types=return_types.return_types,
        )

    def parse_oop(self, code: str, function_data: FunctionData) -> \
            List[FunctionOOP]:
        """
        Parses given code
        """
        if code is None:
            return []

        parser = OOPTokenizer(code)
        tokenized = parser.tokenize()

        colors = colorize_oop_token_list(tokenized)
        if self.context.verbose:
            print(f'[V] {code: <175}', f'[V] {colors: <175}\n', sep='\n')

        oop_metadata = OOPParser(tokenized).parse()
        method = FilterParseFunctionOOP.prepare_oop_method(
            oop_metadata,
            function_data
        )
        field = FilterParseFunctionOOP.prepare_oop_fiel(
            oop_metadata,
            function_data.signature.return_types
        )

        return [FunctionOOP(
            description=oop_metadata.misc_description,
            base_function_name=function_data.name,
            class_name=oop_metadata.method_data.class_name,
            is_static=oop_metadata.method_data.is_static,
            method=method,
            field=field,
        )]

    def pick_oop_container(self, f_name: str, raw_data: str,
                           wiki: WikiText) -> str:
        """
        Picks media wiki code, containing OOP definition
        """
        syntax_picker = WikiGetSyntaxSection(self.context_data, f_name,
                                             raw_data, wiki)
        syntax_picker.get()
        code_inside = syntax_picker.pick_text()

        return code_inside

    def pick_oop(self, f_name: str, raw_data: str, wiki: WikiText) -> \
            Optional[str]:
        """
        Picks out function signature code from an entire data
        """
        container = self.pick_oop_container(f_name, raw_data, wiki)

        signature_match = re.search(self.OOP_REGEX, container)
        if signature_match is None:
            print(
                f'\u001b[33m[WARN] \u001b[0mOOP'
                f' Definition not found "{f_name}"\u001b[0m'
            )
            return

        signature = signature_match.group(1)
        if len(signature.split('\n')) > 1:
            print(
                f'\u001b[33m[WARN] \u001b[0mMultiple '
                f'lines in OOP definition "{f_name}"\u001b[0m'
            )

        return signature.strip()

    def apply(self):
        print('\n\n ============ Parse OOP ============')

        for f_name in self.context_data.parsed:
            raw_content = self.context_data.side_data[f_name]
            wiki_content = self.context_data.wiki_side[f_name]

            data = CompoundOOPData(
                client=self.parse_oop(
                    self.pick_oop(f_name, raw_content.client,
                                  wiki_content.client),
                    self.context_data.parsed[f_name].client[0],
                ) if raw_content.client is not None else [],
                server=self.parse_oop(
                    self.pick_oop(f_name, raw_content.server,
                                  wiki_content.server),
                    self.context_data.parsed[f_name].server[0],
                ) if raw_content.server is not None else [],
            )

            self.context.oops[f_name] = data

        print('Function signature parsing complete\u001b[0m')
