import re
from typing import Optional

from wikitextparser import WikiText, Section

from to_python.core.context import ParseFunctionSide, ContextData
from to_python.core.filter import FilterAbstract
from to_python.core.format import colorize_token_list
from to_python.core.signature import SignatureParser, SignatureTokenizer
from to_python.core.types import FunctionSignature
from to_python.filters.data_list.doc import FilterParseDocs


class WikiGetSyntaxSection:
    """
    Picks a syntax section from wiki page
    """

    # TODO: Think about transforming that utility class into a filter

    def __init__(self, context: ContextData, f_name: str, raw_data: str,
                 wiki: WikiText):
        self.context = context
        self.f_name = f_name
        self.raw_data = raw_data
        self.wiki = wiki

        self.section_index = 0
        self.start_index = 0
        self.section: Optional[Section] = None

    def no_syntax_section(self):
        """
        Process situation, when the Syntax section have not been found
        """
        if self.context.side_data[self.f_name].side != \
                ParseFunctionSide.SHARED:
            print(
                f'\u001b[33m[WARN] \u001b[0m'
                f'No Syntax section "{self.f_name}"\u001b[0m'
            )

    def multiple_syntax_section(self, section_list):
        """
        Process situation, when the Syntax section
          have been found multiple time
        """
        if len(section_list) != 1:
            print(
                f'\u001b[33m[WARN] \u001b[0m'
                f'Multiple Syntax sections "{self.f_name}". \u001b[0m\n'
                f'\u001b[33m[WARN] \u001b[0m'
                f'Selecting the first:\u001b[0m'
            )
            for section, index in section_list:
                print(f'    \u001b[34m{index: 2}.\u001b[0m {section.title}')

        self.section, self.section_index = section_list[0]
        self.start_index = self.section.span[0]

    def get(self, paragraph_title_part: str = 'syntax') -> Optional[Section]:
        """
        Finds syntax section in wiki page (or part of wiki page)
        :return:
        """
        syntax = FilterParseDocs.get_sections_title_contains(
            self.wiki,
            paragraph_title_part
        )
        if not syntax:
            self.no_syntax_section()
        else:
            self.multiple_syntax_section(syntax)

        return self.section

    def pick_text(self) -> str:
        try:
            next_section: Optional[WikiText] = self.wiki.sections[
                self.section_index + 1]
        except IndexError:
            next_section = None

        if next_section is None:
            end_index = len(str(self.wiki))
        else:
            end_index = next_section.span[0]

        return str(self.wiki)[self.start_index:end_index]


class FilterParseFunctionSignature(FilterAbstract):
    """
    Parses function signature
    """

    def __init__(self):
        super().__init__('functions')

    @staticmethod
    def clean_code(code: str) -> str:
        lines = code.split('\n')
        for i, line in enumerate(lines):
            line = re.sub(r'--.+$', '', line)

            lines[i] = line.strip()

        return ' '.join(lines)

    def parse_signature(self, code: str) -> FunctionSignature:
        """
        Parses given code
        """
        code = self.clean_code(code)

        tokenized = SignatureTokenizer(code).tokenize()

        if self.context.verbose:
            colors = colorize_token_list(tokenized)
            print(f'[V] {code: <175}', f'[V] {colors: <175}\n', sep='\n')

        return SignatureParser(
            tokenized=tokenized
        ).parse()

    def pick_signature_container(self, f_name: str, raw_data: str,
                                 wiki: WikiText) -> str:
        """
        Picks media wiki code, containing signature
        """
        syntax_picker = WikiGetSyntaxSection(self.context_data, f_name,
                                             raw_data, wiki)
        syntax_picker.get()
        code_inside = syntax_picker.pick_text()

        if 'syntaxhighlight' not in code_inside:
            raise RuntimeError(
                f'[ERROR] Result media wiki code '
                f'does not contain signature. "{f_name}"'
            )

        return code_inside

    SELECT_CODE_REGEX = re.compile(
        r'<syntaxhighlight[^>]*lua[^>]*>([\s\S]+?)</syntaxhighlight>')

    def pick_signature(self, f_name: str, raw_data: str, wiki: WikiText) -> \
            str:
        """
        Picks out function signature code from an entire data
        """
        container = self.pick_signature_container(f_name, raw_data, wiki)
        signature = re.search(self.SELECT_CODE_REGEX, container).group(1)
        return signature.strip()

    def apply(self):
        print('\n\n ============ Parse Functions ============')

        for f_name in self.context_data.parsed:
            raw_content = self.context_data.side_data[f_name]
            wiki_content = self.context_data.wiki_side[f_name]

            if raw_content.client is not None:
                self.context_data.parsed[f_name].client[
                    0].signature = self.parse_signature(
                    self.pick_signature(f_name, raw_content.client,
                                        wiki_content.client)
                )

            if raw_content.server is not None:
                self.context_data.parsed[f_name].server[
                    0].signature = self.parse_signature(
                    self.pick_signature(f_name, raw_content.server,
                                        wiki_content.server)
                )

        print('Function signature parsing complete\u001b[0m')
