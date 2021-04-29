from typing import Optional

import wikitextparser as wtp

from to_python.core.context import WikiSide
from to_python.core.filter import FilterAbstract


class FilterWikiTextParser(FilterAbstract):
    def parse(self, code: Optional[str]) -> Optional[wtp.WikiText]:
        if code is None:
            return None

        return wtp.parse(code)

    def apply(self):
        for f_name in self.context.raw_data:
            self.context.wiki_raw[f_name] = self.parse(self.context.raw_data[f_name])

        for f_name in self.context.side_data:
            data = self.context.side_data[f_name]
            self.context.wiki_side[f_name] = WikiSide(side=data.side,
                                              server=self.parse(data.server),
                                              client=self.parse(data.client))
