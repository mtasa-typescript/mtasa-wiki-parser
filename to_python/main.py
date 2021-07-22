from to_python.chain import FILTER_CHAIN
from to_python.core.context import Context, ContextData


def main():
    context = Context(functions=ContextData(),
                      events=ContextData(), )

    for filt in FILTER_CHAIN:
        filt.initialize(context)
        filt.apply()

    print('Complete')


if __name__ == '__main__':
    main()