from typing import List

from to_python.core.oop import OOPTokenizer
from to_python.core.signature import SignatureTokenizer

POSTFIX = '\033[0m'

# Generate styles
PREFIX_LIST_GEN = [
    [i, j, k, l]
    for k in [None, 3]  # italic
    for j in [None, 1]  # bold
    for l in [None, 4]  # underline
    for i in [*[i for i in range(90, 97)], 0]  # colors
]

PREFIX_LIST = []
for element in PREFIX_LIST_GEN:
    mixin_start = '\033['
    mixin_end = 'm'

    result = ''
    for sub in element:
        if sub is None:
            continue

        result += mixin_start + str(sub) + mixin_end

    PREFIX_LIST.append(result)


def colorize_token_list(token_list: List[SignatureTokenizer.Token]) -> str:
    token_type_mapping = {
        SignatureTokenizer.TokenType.RETURN_TYPE: PREFIX_LIST[12],
        SignatureTokenizer.TokenType.FUNCTION_NAME: PREFIX_LIST[3],
        SignatureTokenizer.TokenType.ARGUMENT_START: PREFIX_LIST[7],
        SignatureTokenizer.TokenType.ARGUMENT_END: PREFIX_LIST[7],
        SignatureTokenizer.TokenType.ARGUMENT_TYPE: PREFIX_LIST[4],
        SignatureTokenizer.TokenType.ARGUMENT_NAME: PREFIX_LIST[5],
        SignatureTokenizer.TokenType.OPTIONAL_START: PREFIX_LIST[1],
        SignatureTokenizer.TokenType.OPTIONAL_END: PREFIX_LIST[1],
        SignatureTokenizer.TokenType.EQUAL_SIGN: PREFIX_LIST[6],
        SignatureTokenizer.TokenType.DEFAULT_VALUE: PREFIX_LIST[11],
        SignatureTokenizer.TokenType.COMMA_SIGN: PREFIX_LIST[2],
        SignatureTokenizer.TokenType.TYPE_UNION_SIGN: PREFIX_LIST[11],
        SignatureTokenizer.TokenType.VARARGS_SIGN: PREFIX_LIST[12],
        SignatureTokenizer.TokenType.VARARGS_RETURN_SIGN: PREFIX_LIST[13],
    }

    return ' '.join([
        token_type_mapping[element.type] + element.value + POSTFIX
        for element in token_list
    ])


def colorize_oop_token_list(token_list: List[SignatureTokenizer.Token]) -> str:
    token_type_mapping = {
        OOPTokenizer.TokenType.START: PREFIX_LIST[12],
        OOPTokenizer.TokenType.END: PREFIX_LIST[3],
        OOPTokenizer.TokenType.DELIMITER: PREFIX_LIST[7],
        OOPTokenizer.TokenType.UNUSED: PREFIX_LIST[7],
        OOPTokenizer.TokenType.REFERENCE_START: PREFIX_LIST[4],
        OOPTokenizer.TokenType.REFERENCE_BODY: PREFIX_LIST[5],
        OOPTokenizer.TokenType.REFERENCE_END: PREFIX_LIST[1],
        OOPTokenizer.TokenType.NOTE: PREFIX_LIST[1],
        OOPTokenizer.TokenType.METHOD: PREFIX_LIST[6],
        OOPTokenizer.TokenType.FIELD: PREFIX_LIST[11],
        OOPTokenizer.TokenType.COUNTERPART_METHOD: PREFIX_LIST[2],
        OOPTokenizer.TokenType.UNDEFINED: PREFIX_LIST[11],
    }

    return ' '.join([
        token_type_mapping[element.type] + element.value + POSTFIX
        for element in token_list
    ])
