from typing import Optional, Tuple, Set

from crawler.core.types import ListType

HOST_URL: str
BATCH_SIZE: int

FUNCTION_START_FROM: Optional[Tuple[ListType, str]]
FUNCTION_BLACKLIST: Set[str]

EVENT_START_FROM: Optional[Tuple[ListType, str]]
EVENT_BLACKLIST: Set[str]

# URL to MTASA Wiki
HOST_URL = 'https://wiki.multitheftauto.com'

# Amount of pages, that will be fetched per a one request
# The limit is 50
BATCH_SIZE = 50

# What function will be the start point.
# (ListType.SERVER, 'setMarkerType'), for example, will start from the setMarkerType function
# Set None to start from the beginning
FUNCTION_START_FROM = \
    None

# Functions with non-standard wiki pages
FUNCTION_BLACKLIST = {
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

# What event will be the start point (for fetching function).
# (ListType.SERVER, 'onMarkerHit'), for example, will start from the onMarkerHit event
# Set None to start from the beginning
EVENT_START_FROM = \
    None

# Events with non-standard wiki pages
EVENT_BLACKLIST = []
