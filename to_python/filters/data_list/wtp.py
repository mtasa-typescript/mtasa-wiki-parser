from typing import Optional

import wikitextparser as wtp

from to_python.core.context import WikiSide
from to_python.core.filter import FilterAbstract


class FilterWikiTextParser(FilterAbstract):
    def __init__(self, context_type: str):
        """
        :param context_type: `functions` or `events`
        """
        super().__init__()

        self.context_type = context_type

    @staticmethod
    def parse(code: Optional[str]) -> Optional[wtp.WikiText]:
        if code is None:
            return None

        return wtp.parse(code)

    def apply(self):
        context = getattr(self.context, self.context_type)
        for f_name in context.raw_data:
            context.wiki_raw[f_name] = self.parse(context.raw_data[f_name])

        for f_name in context.side_data:
            data = context.side_data[f_name]
            context.wiki_side[f_name] = WikiSide(side=data.side,
                                                      server=self.parse(data.server),
                                                      client=self.parse(data.client))
