from typing import Optional

import wikitextparser as wtp

from to_python.core.context import WikiSide
from to_python.core.filter import FilterAbstract


class FilterWikiTextParser(FilterAbstract):
    def __init__(self, context_type: str):
        """
        :param context_type: `functions` or `events`
        """
        super().__init__(context_type)

    @staticmethod
    def parse(code: Optional[str]) -> Optional[wtp.WikiText]:
        if code is None:
            return None

        return wtp.parse(code)

    def apply(self):
        for f_name in self.context_data.raw_data:
            self.context_data.wiki_raw[f_name] = self.parse(
                self.context_data.raw_data[f_name])

        for f_name in self.context_data.side_data:
            data = self.context_data.side_data[f_name]
            self.context_data.wiki_side[f_name] = WikiSide(side=data.side,
                                                           server=self.parse(
                                                               data.server),
                                                           client=self.parse(
                                                               data.client))

        print('Wiki Text Parse complete\u001b[0m')
