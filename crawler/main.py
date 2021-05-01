from crawler import config
from crawler.chain import FILTER_CHAIN
from crawler.core.filter import Context


def main():
    context = Context(host_url=config.HOST_URL,
                      fetch_start_from=config.START_FROM,
                      blacklist=config.BLACKLIST,
                      url_list=[],
                      fetched=[])

    for filt in FILTER_CHAIN:
        filt.initialize(context)
        filt.apply()

    print('Complete')


if __name__ == '__main__':
    main()
