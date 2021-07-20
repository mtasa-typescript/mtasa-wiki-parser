import re

from wikitextparser import WikiText

from to_python.core.context import ContextData
from to_python.core.filter import FilterAbstract
from to_python.core.format import colorize_token_list
from to_python.core.signature import SignatureParser, SignatureTokenizer
from to_python.core.types import FunctionArgumentValues, CompoundEventData
from to_python.filters.data_list.signature import WikiGetSyntaxSection, FilterParseFunctionSignature


class FilterParseEventSignature(FilterAbstract):
    """
    Parses function signature
    """

    def __init__(self):
        super().__init__('events')

    def parse_signature(self, code: str) -> FunctionArgumentValues:
        """
        Parses given code
        """
        code = FilterParseFunctionSignature.clean_code(code)

        # Workaround: wrap parameters into a function, tokenize and then inject arguments only
        code = f'void eventCallback( {code} )'

        tokenized = SignatureTokenizer(code).tokenize()

        colors = colorize_token_list(tokenized)
        print(f'{code: <175}', f'{colors: <175}\n', sep='\n')

        function_signature = SignatureParser(
            tokenized=tokenized
        ).parse()

        return function_signature.arguments

    def pick_signature_container(self, f_name: str, raw_data: str, wiki: WikiText) -> str:
        """
        Picks media wiki code, containing signature
        """
        syntax_picker = WikiGetSyntaxSection(self.context_data, f_name, raw_data, wiki)
        syntax_picker.get('parameters')
        code_inside = syntax_picker.pick_text()

        if 'syntaxhighlight' not in code_inside:
            code_inside_lower = code_inside.lower()
            if 'no parameters' in code_inside_lower or 'none' in code_inside_lower:
                return '<syntaxhighlight lang="lua"> </syntaxhighlight>'

            raise RuntimeError(f'[ERROR] Result media wiki code does not contain signature. "{f_name}"')

        return code_inside

    def pick_signature(self, f_name: str, raw_data: str, wiki: WikiText) -> str:
        """
        Picks out function signature code from an entire data
        """
        container = self.pick_signature_container(f_name, raw_data, wiki)
        signature = re.search(FilterParseFunctionSignature.SELECT_CODE_REGEX, container).group(1)
        return signature.strip()

    def apply(self):
        self.context_data: ContextData[CompoundEventData]
        print('\n\n ============ Parse Events ============')

        for f_name in self.context_data.parsed:
            raw_content = self.context_data.side_data[f_name]
            wiki_content = self.context_data.wiki_side[f_name]

            if raw_content.client is not None:
                self.context_data.parsed[f_name].client[0].arguments = self.parse_signature(
                    self.pick_signature(f_name, raw_content.client, wiki_content.client)
                )

            if raw_content.server is not None:
                self.context_data.parsed[f_name].server[0].arguments = self.parse_signature(
                    self.pick_signature(f_name, raw_content.server, wiki_content.server)
                )
