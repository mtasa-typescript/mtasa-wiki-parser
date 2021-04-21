import enum
from dataclasses import dataclass


class ListType(enum.Enum):
    CLIENT = 'Client'
    SERVER = 'Server'

    def __repr__(self) -> str:
        if self == self.CLIENT:
            return 'ListType.CLIENT'
        if self == self.SERVER:
            return 'ListType.SERVER'


@dataclass
class FunctionUrl:
    url: str
    name: str
    category: str
    function_type: ListType

    def get_full_url(self) -> str:
        from crawler.config import HOST_URL
        return f'{HOST_URL}{self.url}'
