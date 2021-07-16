import sys
from typing import List, Callable

from crawler import config
from crawler.chain import get_filter_chain, get_event_filter_chain
from crawler.core.filter import Context, FilterAbstract


def main(filter_chain: Callable[[Context], List[FilterAbstract]]):
    context = Context(host_url=config.HOST_URL,
                      fetch_start_from=config.FUNCTION_START_FROM,
                      fetch_batch_size=config.BATCH_SIZE,
                      blacklist=config.FUNCTION_BLACKLIST,
                      event_fetch_start_from=config.EVENT_START_FROM,
                      event_blacklist=config.EVENT_BLACKLIST, )

    print('Start filter chain')
    for filt in filter_chain(context):
        filt.initialize(context)
        filt.apply()

    print('Complete')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Expected 1 argv: [functions/events]', file=sys.stderr)
        exit(1)

    main(get_filter_chain if sys.argv[1] == 'functions' else get_event_filter_chain)
