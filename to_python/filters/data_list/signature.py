import enum
import re
import sys
from dataclasses import dataclass
from typing import Optional, List

from wikitextparser import WikiText

from to_python.core.context import ParseFunctionSide
from to_python.core.filter import FilterAbstract
from to_python.core.format import colorize_token_list
from to_python.core.signature import SignatureParser, SignatureTokenizer
from to_python.core.types import FunctionType
from to_python.filters.data_list.doc import FilterParseDocs


class FilterParseFunctionSignature(FilterAbstract):
    """
    Parses function signature
    """

    @staticmethod
    def clean_code(code: str) -> str:
        lines = code.split('\n')
        for i, line in enumerate(lines):
            line = re.sub(r'--.+$', '', line)

            lines[i] = line.strip()

        return ' '.join(lines)

    def parse_signature(self, code: str) -> FunctionType:
        """
        Parses given code
        """
        code = self.clean_code(code)

        tokenized = SignatureTokenizer(code).tokenize()

        colors = colorize_token_list(tokenized)
        print(f'{code: <175}', f'{colors: <175}', sep="\n" if len(code) > 175 else " ")

        result = SignatureParser(
            tokenized=tokenized
        ).parse()

    def pick_signature_container(self, f_name: str, raw_data: str, wiki: WikiText) -> str:
        """
        Picks media wiki code, containing signature
        """
        syntax = FilterParseDocs.get_sections_title_contains(wiki, 'syntax')
        if not syntax:
            if self.context.side_data[f_name].side != ParseFunctionSide.SHARED:
                print(f'[WARN] No Syntax section "{f_name}"', file=sys.stderr)
            syntax_index = 0
            start_index = 0

        else:
            if len(syntax) != 1:
                print(f'[WARN] Multiple Syntax sections "{f_name}". \n[WARN] Selecting the first:', file=sys.stderr)
                for section, index in syntax:
                    print(f'    {index: 2}. {section.title}', file=sys.stderr)

            syntax, syntax_index = syntax[0]
            start_index = syntax.span[0]

        try:
            next_section: Optional[WikiText] = wiki.sections[syntax_index + 1]
        except IndexError:
            next_section = None

        if next_section is None:
            end_index = len(str(wiki))
        else:
            end_index = next_section.span[0]

        code_inside = str(wiki)[start_index:end_index]
        if 'syntaxhighlight' not in code_inside:
            raise RuntimeError(f'[ERROR] Result media wiki code does not contain signature. "{f_name}"')

        return code_inside

    SELECT_CODE_REGEX = re.compile(r'<syntaxhighlight[^>]*>([\s\S]+?)</syntaxhighlight>')

    def pick_signature(self, f_name: str, raw_data: str, wiki: WikiText) -> str:
        """
        Picks out function signature code from an entire data
        """
        container = self.pick_signature_container(f_name, raw_data, wiki)
        signature = re.search(self.SELECT_CODE_REGEX, container).group(1)
        return signature.strip()

    def apply(self):
        for f_name in self.context.parsed:
            raw_content = self.context.side_data[f_name]
            wiki_content = self.context.wiki_side[f_name]

            if raw_content.client is not None:
                self.context.parsed[f_name].client.signature = self.parse_signature(
                    self.pick_signature(f_name, raw_content.client, wiki_content.client)
                )

            if raw_content.server is not None:
                self.context.parsed[f_name].server.signature = self.parse_signature(
                    self.pick_signature(f_name, raw_content.server, wiki_content.server)
                )
