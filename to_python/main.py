from to_python.chain import FILTER_CHAIN
from to_python.core.context import Context


def main():
    context = Context(functions=dict(),
                      parsed=dict(),
                      raw_data=dict(),
                      side_data=dict(),
                      data=dict(),
                      wiki_raw=dict(),
                      wiki_side=dict(), )

    for filt in FILTER_CHAIN:
        filt.initialize(context)
        filt.apply()

    print('Complete')


if __name__ == '__main__':
    main()
