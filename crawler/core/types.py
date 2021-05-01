import enum
from dataclasses import dataclass


class ListType(enum.Enum):
    CLIENT = 'Client'
    SERVER = 'Server'

    def __repr__(self) -> str:
        return str(self)


@dataclass
class FunctionUrl:
    url: str
    name: str
    category: str
    function_type: ListType

    def get_full_url(self) -> str:
        from crawler.config import HOST_URL
        return f'{HOST_URL}{self.url}'

    def __repr__(self):
        return f'''FunctionUrl(
        url="{self.url}",
        name="{self.name}",
        category="{self.category}",
        function_type={repr(self.function_type)},
    )'''
