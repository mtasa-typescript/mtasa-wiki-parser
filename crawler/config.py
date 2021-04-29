from typing import Optional, Tuple, Set

from crawler.core.types import ListType

HOST_URL: str
START_FROM: Optional[Tuple[ListType, str]]
BLACKLIST: Set[str]

# URL to MTASA Wiki
HOST_URL = 'https://wiki.multitheftauto.com'

# What function will be the start point.
# (ListType.SERVER, 'setMarkerType'), for example, will start from the setMarkerType function
# Set None to start from the beginning
START_FROM = \
    None

# Functions with non-standard wiki pages
BLACKLIST = {
    'Matrix',
    'Vector/Vector2',
    'Vector/Vector3',
    'Vector/Vector4',

    'httpClear',
    'httpRequestLogin',
    'httpSetResponseCode',
    'httpSetResponseCookie',
    'httpSetResponseHeader',
    'httpWrite',

    'utf8.lower',
    'utf8.upper',
}