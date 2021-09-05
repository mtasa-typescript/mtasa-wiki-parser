import re
from typing import Optional

from to_python.core.context import ParseFunctionSide, RawSide
from to_python.core.filter import FilterAbstract
from to_python.core.types import EventData, CompoundEventData
from to_python.filters.data_list.side import FilterParseFunctionSide


class FilterParseSideSharedFileSectionsInvalid(RuntimeError):
    pass


class FilterParseEventSide(FilterAbstract):
    """
    Determines function side (client/server/shared).
    Puts client and server content into context.side_data
    """
    CLIENT_SIGNATURE = re.compile(r'client[_ ]event', re.IGNORECASE)
    SERVER_SIGNATURE = re.compile(r'server[_ ]event', re.IGNORECASE)

    def __init__(self):
        super().__init__('events')

    @staticmethod
    def get_side_from_line(line: str) -> Optional[ParseFunctionSide]:
        line = FilterParseFunctionSide.line_process(line)

        if not line.startswith('{{'):
            return None

        if 'event' not in line:
            return None

        if re.search(FilterParseEventSide.CLIENT_SIGNATURE, line):
            return ParseFunctionSide.CLIENT
        if re.search(FilterParseEventSide.SERVER_SIGNATURE, line):
            return ParseFunctionSide.SERVER

    def get_file_side(self, raw: str) -> ParseFunctionSide:
        """
        Determines file's side
        :param raw: Raw data
        """

        for line in raw.split('\n'):
            side = self.get_side_from_line(line)
            if side is None:
                continue

            return side

        raise RuntimeError('Cannot find event type')

    def parse_file(self, name: str) -> RawSide:
        """
        Parses file (by filename)
        """

        raw = self.context_data.raw_data[name]
        side = self.get_file_side(raw)

        if side == ParseFunctionSide.CLIENT:
            return RawSide(side=side,
                           server=None,
                           client=raw)

        if side == ParseFunctionSide.SERVER:
            return RawSide(side=side,
                           server=raw,
                           client=None)

    def apply(self):
        for name in self.context_data.parsed:
            data = self.parse_file(name)
            self.context_data.side_data[name] = data

            # Init parsed data objects
            kwargs = dict()
            if data.client is not None:
                kwargs['client'] = [EventData(None, None, name)]
            if data.server is not None:
                kwargs['server'] = [EventData(None, None, name)]
            self.context_data.parsed[name] = CompoundEventData(**kwargs)

        print('Parse event side complete\u001b[0m')
