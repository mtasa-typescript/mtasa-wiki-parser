import re
import sys
from typing import Optional

from wikitextparser import WikiText

from to_python.core.filter import FilterAbstract
from to_python.core.format import colorize_oop_token_list
from to_python.core.oop import OOPTokenizer, OOPParser
from to_python.core.types import FunctionOOP
from to_python.filters.data_list.signature import WikiGetSyntaxSection


class FilterParseFunctionOOP(FilterAbstract):
    OOP_REGEX = re.compile(r'(\{\{OOP.*\}\})', re.IGNORECASE)

    def parse_oop(self, code: str) -> Optional[FunctionOOP]:
        """
        Parses given code
        """
        if code is None:
            return None

        parser = OOPTokenizer(code)
        tokenized = parser.tokenize()

        colors = colorize_oop_token_list(tokenized)
        print(f'{code: <175}', f'{colors: <175}\n', sep='\n')

        return OOPParser(tokenized).parse()

    def pick_oop_container(self, f_name: str, raw_data: str, wiki: WikiText) -> str:
        """
        Picks media wiki code, containing OOP definition
        """
        syntax_picker = WikiGetSyntaxSection(self.context, f_name, raw_data, wiki)
        syntax_picker.get()
        code_inside = syntax_picker.pick_text()

        return code_inside

    def pick_oop(self, f_name: str, raw_data: str, wiki: WikiText) -> Optional[str]:
        """
        Picks out function signature code from an entire data
        """
        container = self.pick_oop_container(f_name, raw_data, wiki)

        signature_match = re.search(self.OOP_REGEX, container)
        if signature_match is None:
            print(f'[WARN] OOP Definition not found "{f_name}"', file=sys.stderr)
            return

        signature = signature_match.group(1)
        if len(signature.split('\n')) > 1:
            print(f'[WARN] Multiple lines in OOP definition "{f_name}"', file=sys.stderr)

        return signature.strip()

    def apply(self):
        print('\n\n ============ Parse OOP ============')

        for f_name in self.context.parsed:
            raw_content = self.context.side_data[f_name]
            wiki_content = self.context.wiki_side[f_name]

            if raw_content.client is not None:
                self.context.parsed[f_name].client.oop = self.parse_oop(
                    self.pick_oop(f_name, raw_content.client, wiki_content.client)
                )

            if raw_content.server is not None:
                self.context.parsed[f_name].server.oop = self.parse_oop(
                    self.pick_oop(f_name, raw_content.server, wiki_content.server)
                )
