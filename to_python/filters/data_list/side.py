import re
from typing import Optional

from to_python.core.filter import FilterAbstract, ParseFunctionSide, RawSide


class FilterParseSideSharedFileSectionsInvalid(RuntimeError):
    pass


class FilterParseSide(FilterAbstract):
    """
    Determines function side (client/server/shared).
    Puts client and server content into context.side_data
    """

    SHARED_SIGNATURE = re.compile(r'(server[_ ]client|shared)[_ ]function', re.IGNORECASE)
    CLIENT_SIGNATURE = re.compile(r'client[_ ]function', re.IGNORECASE)
    SERVER_SIGNATURE = re.compile(r'server[_ ]function', re.IGNORECASE)

    SERVER_SECTION = re.compile(r'<section.+class="server".*?>([\s\S]+?)<\/section>', re.IGNORECASE)
    CLIENT_SECTION = re.compile(r'<section.+class="client".*?>([\s\S]+?)<\/section>', re.IGNORECASE)

    @staticmethod
    def line_process(line: str) -> str:
        line = line.strip().lower()

        cut_comment = re.search(r'}}', line)
        if cut_comment:
            line = line[:cut_comment.start()]

        return line  # Cut comments

    @staticmethod
    def get_side_from_line(line: str) -> Optional[ParseFunctionSide]:
        line = FilterParseSide.line_process(line)

        if not line.startswith('{{'):
            return None

        if 'function' not in line:
            return None

        if re.search(FilterParseSide.SHARED_SIGNATURE, line):
            return ParseFunctionSide.SHARED
        if re.search(FilterParseSide.CLIENT_SIGNATURE, line):
            return ParseFunctionSide.CLIENT
        if re.search(FilterParseSide.SERVER_SIGNATURE, line):
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

        raise RuntimeError('Cannot find function type')

    def parse_shared_file(self, raw: str) -> RawSide:
        """
        Parse raw data, if file is shared
        """
        if len(re.findall('<section', raw)) < 2:
            return RawSide(side=ParseFunctionSide.SHARED,
                           server=raw,
                           client=raw)
        server_raw = re.search(self.SERVER_SECTION, raw)
        if not server_raw:
            raise FilterParseSideSharedFileSectionsInvalid('"Server" section not found')

        client_raw = re.search(self.CLIENT_SECTION, raw)
        if not client_raw:
            raise FilterParseSideSharedFileSectionsInvalid('"Client" section not found')

        server_raw = server_raw.group(1)
        client_raw = client_raw.group(1)

        return RawSide(side=ParseFunctionSide.SHARED,
                       server=server_raw,
                       client=client_raw)

    def parse_file(self, name: str) -> RawSide:
        """
        Parses file (by filename)
        """

        raw = self.context.raw_data[name]
        side = self.get_file_side(raw)

        if side == ParseFunctionSide.SHARED:
            return self.parse_shared_file(raw)
        elif side == ParseFunctionSide.CLIENT:
            return RawSide(side=side,
                           server=None,
                           client=raw)
        elif side == ParseFunctionSide.SERVER:
            return RawSide(side=side,
                           server=raw,
                           client=None)

    def apply(self):
        for name in self.context.parsed:
            self.context.side_data[name] = self.parse_file(name)
