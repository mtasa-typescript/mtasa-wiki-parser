from typing import List

from to_python.core.signature import SignatureTokenizer


def colorize_token_list(token_list: List[SignatureTokenizer.Token]) -> str:
    postfix = '\033[0m'

    # Generate styles
    prefix_list_gen = [
        [i, j, k, l]
        for k in [None, 3]  # italic
        for j in [None, 1]  # bold
        for l in [None, 4]  # underline
        for i in [*[i for i in range(90, 97)], 0]  # colors
    ]

    prefix_list = []
    for element in prefix_list_gen:
        mixin_start = '\033['
        mixin_end = 'm'

        result = ''
        for sub in element:
            if sub is None:
                continue

            result += mixin_start + str(sub) + mixin_end

        prefix_list.append(result)

    token_type_mapping = {
        SignatureTokenizer.TokenType.RETURN_TYPE: prefix_list[12],
        SignatureTokenizer.TokenType.FUNCTION_NAME: prefix_list[3],
        SignatureTokenizer.TokenType.ARGUMENT_START: prefix_list[7],
        SignatureTokenizer.TokenType.ARGUMENT_END: prefix_list[7],
        SignatureTokenizer.TokenType.ARGUMENT_TYPE: prefix_list[4],
        SignatureTokenizer.TokenType.ARGUMENT_NAME: prefix_list[5],
        SignatureTokenizer.TokenType.OPTIONAL_START: prefix_list[1],
        SignatureTokenizer.TokenType.OPTIONAL_END: prefix_list[1],
        SignatureTokenizer.TokenType.EQUAL_SIGN: prefix_list[6],
        SignatureTokenizer.TokenType.DEFAULT_VALUE: prefix_list[11],
        SignatureTokenizer.TokenType.COMMA_SIGN: prefix_list[2],
        SignatureTokenizer.TokenType.TYPE_UNION_SIGN: prefix_list[11],
        SignatureTokenizer.TokenType.VARARGS_SIGN: prefix_list[12],
        SignatureTokenizer.TokenType.VARARGS_RETURN_SIGN: prefix_list[13],
    }

    return ' '.join([
        token_type_mapping[element.type] + element.value + postfix
        for element in token_list
    ])
