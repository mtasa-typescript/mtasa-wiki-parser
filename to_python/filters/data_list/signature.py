from typing import Optional

from wikitextparser import WikiText

from to_python.core.filter import FilterAbstract
from to_python.core.types import FunctionType
from to_python.filters.data_list.doc import FilterParseDocs


class FilterParseFunctionSignature(FilterAbstract):
    """
    Parses function signature
    """

    def parse_signature(self, code: str) -> FunctionType:
        """
        Parses given code
        """
        pass

    def pick_signature(self, raw_data: str, wiki: WikiText) -> str:
        """
        Picks out function signature code from an entire data
        """
        syntax = FilterParseDocs.get_sections_title_contains(wiki, 'syntax')
        if len(syntax) != 1:
            raise RuntimeError('')

        syntax = syntax[0]
        syntax_index = wiki.sections.index(syntax)
        # FIXME : DEBUG THAT

        try:
            next_section: Optional[WikiText] = wiki.sections[syntax_index + 1]
        except IndexError:
            next_section = None

        if next_section is None:
            end_index = len(str(wiki))
        else:
            end_index = next_section.span[0]

        code_inside = str(wiki)[syntax.span[0]:end_index]

        print(raw_data, wiki)

    def apply(self):
        for f_name in self.context.parsed:
            raw_content = self.context.side_data[f_name]
            wiki_content = self.context.wiki_side[f_name]

            if raw_content.client is not None:
                self.context.parsed[f_name].client.signature = self.parse_signature(
                    self.pick_signature(raw_content.client, wiki_content.client)
                )

            if raw_content.server is not None:
                self.context.parsed[f_name].server.signature = self.parse_signature(
                    self.pick_signature(raw_content.server, wiki_content.server)
                )
