from crawler import config
from to_typescript.chain import FILTER_CHAIN
from to_typescript.core.context import Context


def main():
    context = Context(host_name=config.HOST_URL)

    for filter_item in FILTER_CHAIN:
        filter_item.initialize(context)
        filter_item.apply()

    print('Complete')


if __name__ == '__main__':
    main()
