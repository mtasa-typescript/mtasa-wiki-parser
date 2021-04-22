from crawler.chain import FILTER_CHAIN
from crawler.core.filter import Context


def main():
    context = Context

    for filter in FILTER_CHAIN:
        filter.initialize()
        filter.apply()

if __name__ == '__main__':
    main()