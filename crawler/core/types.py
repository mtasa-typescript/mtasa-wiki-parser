import enum
from dataclasses import dataclass


class ListType(enum.Enum):
    CLIENT = 'Client'
    SERVER = 'Server'

    def __repr__(self) -> str:
        return str(self)


@dataclass
class PageUrl:
    """
    Describes the URL to the MTASA Wiki function page
    """
    url: str
    name: str
    category: str
    type: ListType

    def get_full_url(self) -> str:
        from crawler.config import HOST_URL
        return f'{HOST_URL}{self.url}'

    def __repr__(self):
        return f'''PageUrl(
        url="{self.url}",
        name="{self.name}",
        category="{self.category}",
        type={repr(self.type)},
    )'''
