from typing import Optional

from crawler.core.types import ListType

HOST_URL: str
START_FROM: Optional[ListType, str]

# URL to MTASA Wiki
HOST_URL = 'https://wiki.multitheftauto.com'

# What function will be the start point.
# [ListType.SERVER, 'fileOpen'], for example, will start from the fileOpen function
# Set None to start from the beginning
START_FROM = \
    None
