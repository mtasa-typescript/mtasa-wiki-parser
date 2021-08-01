import sys
from typing import List

from to_python.chain import FILTER_CHAIN
from to_python.core.context import Context, ContextData


def main(argc: int, argv: List[str]):
    verbose_mode = False

    if argc >= 2:
        verbose_mode = 'v' in argv[1]

    context = Context(functions=ContextData(),
                      events=ContextData(),
                      verbose=verbose_mode)

    for filt in FILTER_CHAIN:
        filt.initialize(context)
        filt.apply()

    print('\u001b[32mComplete\u001b[0m')


if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
