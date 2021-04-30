import enum
import re
import sys
from dataclasses import dataclass
from typing import Optional, List

from to_python.core.types import FunctionType


class SignatureTokenizerError(RuntimeError):
    pass


class SignatureParserError(RuntimeError):
    pass


class SignatureTokenizer:
    """
    Splits code string into tokens.
    Does not change/replace/remove anything from the original string
    """

    CHARS_TO_SPLIT = re.compile(r'([(\[\]=,)/|" ]|\.\.\.)')

    def __init__(self, code: str):
        self.code = code
        self.tokenized: List[SignatureTokenizer.Token] = []

    def token_should_have_type(self, token: 'SignatureTokenizer.Token', token_type: 'SignatureTokenizer.TokenType'):
        if token.type != token_type:
            raise SignatureTokenizerError(f'Expected {str(token_type)} token, got {str(token.type)}. '
                                          f'Function signature:\n{self.code}')

    class TokenType(enum.Enum):
        RETURN_TYPE = 'ReturnType'
        FUNCTION_NAME = 'FunctionName'
        ARGUMENT_START = 'ArgumentStart'
        ARGUMENT_END = 'ArgumentEnd'
        ARGUMENT_TYPE = 'ArgumentType'
        ARGUMENT_NAME = 'ArgumentName'
        OPTIONAL_START = 'OptionalStart'
        OPTIONAL_END = 'OptionalEnd'
        EQUAL_SIGN = 'EqualSign'
        DEFAULT_VALUE = 'DefaultValue'
        COMMA_SIGN = 'CommaSign'
        UNDEFINED = 'Undefined'
        TYPE_UNION_SIGN = 'TypeUnionSign'
        VARARGS_SIGN = 'VarargsSign'
        VARARGS_RETURN_SIGN = 'VarargsReturnSign'

        def __repr__(self) -> str:
            return str(self)

    @dataclass
    class Token:
        type: 'SignatureTokenizer.TokenType'
        value: str

    def split(self):
        """
        Splits self.code by delimiters
        :return: List of splitter strings
        """
        delimiters = [x for x in re.finditer(self.CHARS_TO_SPLIT, self.code)]
        split = []
        last_index = 0
        for delimiter in delimiters:
            end_index = delimiter.span()[0]
            split.append(self.code[last_index:end_index])
            split.append(delimiter.group())

            last_index = delimiter.span()[1]

        split.append(self.code[last_index:])
        return list(filter(lambda x: x != '' and x != ' ', split))

    def fill_tokenize(self, split_list: List[str]):
        """
        Initializes self.tokenized. Determines obvious tokens.
        """
        for token in split_list:
            token_type = self.TokenType.UNDEFINED
            if token == '=':
                token_type = self.TokenType.EQUAL_SIGN
            if token == '[':
                token_type = self.TokenType.OPTIONAL_START
            if token == ']':
                token_type = self.TokenType.OPTIONAL_END
            if token == ',':
                token_type = self.TokenType.COMMA_SIGN
            if token == '(':
                token_type = self.TokenType.ARGUMENT_START
            if token == ')':
                token_type = self.TokenType.ARGUMENT_END
            if token in {'/', '|'}:
                token_type = self.TokenType.TYPE_UNION_SIGN
            if token == '...':
                token_type = self.TokenType.VARARGS_SIGN
            if token == '"':
                token_type = self.TokenType.DEFAULT_VALUE

            self.tokenized.append(self.Token(value=token,
                                             type=token_type))

    def function_name_and_returns_tokenize(self):
        """
        Determines function name and return types
        """
        for index, token in enumerate(self.tokenized):
            if token.type != self.TokenType.ARGUMENT_START:
                continue

            self.token_should_have_type(self.tokenized[index - 1], self.TokenType.UNDEFINED)
            self.tokenized[index - 1].type = self.TokenType.FUNCTION_NAME
            for i in range(0, index - 1):
                in_token = self.tokenized[i]
                if in_token.type in {
                    self.TokenType.TYPE_UNION_SIGN,  # Example: table/xmlnode
                    self.TokenType.COMMA_SIGN,  # Example: STRING, STRING getPedAnimation ( ped thePed )
                    self.TokenType.OPTIONAL_START,
                    self.TokenType.OPTIONAL_END,  # Example: INT, INT [, INT] dxGetMaterialSize
                }:
                    continue

                # Variable return values. Example: VAR... call
                if in_token.type == self.TokenType.VARARGS_SIGN:
                    in_token.type = self.TokenType.VARARGS_RETURN_SIGN
                    continue

                self.token_should_have_type(in_token, self.TokenType.UNDEFINED)
                in_token.type = self.TokenType.RETURN_TYPE

            break

    def default_value_tokenize(self):
        """
        After equal sign there is always a default value
        """
        for index, token in enumerate(self.tokenized):
            if token.type != self.TokenType.EQUAL_SIGN:
                continue

            if self.tokenized[index + 1].type != self.TokenType.DEFAULT_VALUE:
                self.token_should_have_type(self.tokenized[index + 1], self.TokenType.UNDEFINED)
            self.tokenized[index + 1].type = self.TokenType.DEFAULT_VALUE

            # Default value is a function call. Example: getRootElement()
            if self.tokenized[index + 2].type == self.TokenType.ARGUMENT_START:
                for i in range(index + 3, len(self.tokenized)):
                    in_token = self.tokenized[i]
                    if in_token.type == self.TokenType.ARGUMENT_END:
                        in_token.type = self.TokenType.DEFAULT_VALUE
                        break

                    in_token.type = self.TokenType.DEFAULT_VALUE

            # Default value is a formula. Example: vehiclesDistance * 2.14
            for i in range(index + 2, len(self.tokenized)):
                in_token = self.tokenized[i]
                if in_token.type in {self.TokenType.COMMA_SIGN,
                                     self.TokenType.ARGUMENT_END,
                                     self.TokenType.OPTIONAL_END,
                                     self.TokenType.OPTIONAL_START}:
                    break

                in_token.type = self.TokenType.DEFAULT_VALUE

            # Default value is a string. Commas and other chars should be covered. Example: "world,vehicle,object,other"
            if self.tokenized[index + 1].value == '"':
                for i in range(index + 2, len(self.tokenized)):
                    in_token = self.tokenized[i]
                    if in_token.value == '"':
                        break

                    in_token.type = self.TokenType.DEFAULT_VALUE

    def arguments_tokenize(self):
        """
        Tokenizes function arguments.
        After comma sign expected: [optional start/optional end] + type + argument name
        """
        arguments = False

        for index, token in enumerate(self.tokenized):
            # Works only in round brackets (between TokenType.ARGUMENT_START and TokenType.ARGUMENT_END)
            if token.type == self.TokenType.ARGUMENT_START:
                arguments = True
            if token.type == self.TokenType.ARGUMENT_END:
                arguments = False
            if not arguments:
                continue

            # Key tokens
            if token.type not in {
                self.TokenType.COMMA_SIGN,  # ,
                self.TokenType.ARGUMENT_START,  # (
                self.TokenType.TYPE_UNION_SIGN  # Example object theObject / int modelId
            }:
                continue

            if token.type == self.TokenType.TYPE_UNION_SIGN and self.tokenized[index + 1].type not in {
                self.TokenType.UNDEFINED
            }:
                continue

            if self.tokenized[index + 1].type == self.TokenType.ARGUMENT_END:
                break

            current_type = self.TokenType.ARGUMENT_TYPE
            for i in range(index + 1, len(self.tokenized)):
                in_token = self.tokenized[i]
                if in_token.type in {self.TokenType.OPTIONAL_START, self.TokenType.OPTIONAL_END}:
                    continue
                if in_token.type in {
                    self.TokenType.COMMA_SIGN,
                    self.TokenType.VARARGS_SIGN,
                    self.TokenType.ARGUMENT_END
                }:
                    break

                # Type unions. Example: "string / table"
                if in_token.type in {self.TokenType.TYPE_UNION_SIGN} \
                        and current_type == self.TokenType.ARGUMENT_NAME:
                    current_type = self.TokenType.ARGUMENT_TYPE
                    continue

                self.token_should_have_type(self.tokenized[i], self.TokenType.UNDEFINED)
                in_token.type = current_type

                if current_type == self.TokenType.ARGUMENT_TYPE:
                    current_type = self.TokenType.ARGUMENT_NAME
                else:
                    break

        # ARGUMENT_NAME should be before the VARARGS_SIGN
        # Example: [arguments...]
        for index, token in enumerate(self.tokenized):
            if token.type != self.TokenType.VARARGS_SIGN:
                continue

            if self.tokenized[index - 1].type == self.TokenType.ARGUMENT_TYPE:
                self.tokenized[index - 1].type = self.TokenType.ARGUMENT_NAME

            if token.type != self.TokenType.VARARGS_SIGN:
                continue

            if self.tokenized[index - 1].type == self.TokenType.ARGUMENT_TYPE:
                self.tokenized[index - 1].type = self.TokenType.ARGUMENT_NAME

        # VARARGS_SIGN can be used in argument name
        # Example: int amount/weapon/model
        index = 0
        while index < len(self.tokenized):
            token = self.tokenized[index]

            # Capture pair ARG_NAME + TYPE_UNION_SIGN
            if not (token.type == self.TokenType.TYPE_UNION_SIGN and
                    self.tokenized[index - 1].type == self.TokenType.ARGUMENT_NAME):
                index += 1
                continue

            i = index + 1
            while i < len(self.tokenized):
                # expected TYPE + NAME + UNION + TYPE + NAME + UNION + ... + separator (bracket, comma)
                separators = {self.TokenType.COMMA_SIGN,
                              self.TokenType.ARGUMENT_END,
                              self.TokenType.OPTIONAL_END,
                              self.TokenType.OPTIONAL_START}
                if self.tokenized[i].type in separators:
                    break

                arg_name = self.tokenized[i + 1]
                if arg_name.type == self.TokenType.ARGUMENT_NAME:
                    i += 2
                    continue

                # => "token" linked to the argument name
                self.tokenized[i].type = self.TokenType.ARGUMENT_NAME
                self.tokenized[index].type = self.TokenType.ARGUMENT_NAME
                if arg_name.type not in separators:
                    arg_name.type = self.TokenType.ARGUMENT_NAME
                else:
                    i += 2
                    break

                i += 2

            index = i

    def concat_neighbours_tokenize(self):
        """
        Concat neighbor tokens into a single one, if allowed
        """
        allowed = {
            self.TokenType.DEFAULT_VALUE,
            self.TokenType.ARGUMENT_NAME,
        }

        index = 0
        while index < len(self.tokenized):
            token = self.tokenized[index]
            if token.type not in allowed:
                index += 1
                continue

            if self.tokenized[index + 1].type == token.type:
                token.value += self.tokenized[index + 1].value
                self.tokenized.pop(index + 1)
                continue

            index += 1

    def brackets_check(self, exception: bool = True):
        """
        Checks brackets.
        Only one round brackets pair expected
        :param exception Throw an exception, or just print an stderr message
        """
        for open_bracket, close_bracket in [
            (self.TokenType.ARGUMENT_START,
             self.TokenType.ARGUMENT_END),
        ]:
            open_bracket_index = None
            close_bracket_index = None

            for index, token in enumerate(self.tokenized):
                if token.type == open_bracket:
                    if open_bracket_index is not None:
                        message = f'Multiple opened brackets {token.type} on position {index}'
                        if exception:
                            raise SignatureTokenizerError(f'{message}. Function signature:\n{self.code}')
                        else:
                            print(f'[ERROR] {message}')

                    open_bracket_index = index
                    continue

                if token.type == close_bracket:
                    if close_bracket_index is not None:
                        message = f'Multiple closed brackets {token.type} on position {index}'
                        if exception:
                            raise SignatureTokenizerError(f'{message}. Function signature:\n{self.code}')
                        else:
                            print(f'[ERROR] {message}')

                    close_bracket_index = index
                    continue

    def final_check(self):
        """
        Check: there should be no UNDEFINED tokens
        """
        self.brackets_check()

        # No UNDEFINED Tokens
        for index, token in enumerate(self.tokenized):
            if token.type != self.TokenType.UNDEFINED:
                continue
            raise SignatureTokenizerError('Undefined token. Function signature: \n' + self.code)

        # Exactly one FUNCTION_NAME expected
        function_name_counter = 0
        for index, token in enumerate(self.tokenized):
            if token.type != self.TokenType.FUNCTION_NAME:
                continue
            function_name_counter += 1
        if function_name_counter != 1:
            raise SignatureTokenizerError('Expected only one FUNCTION_NAME. Function signature: \n' + self.code)

        # ARGUMENT_TYPE => ARGUMENT_TYPE + [UNION_TYPE SIGN + ARGUMENT_TYPE] + ARGUMENT_NAME in pair expected
        for index, token in enumerate(self.tokenized):
            if token.type != self.TokenType.ARGUMENT_TYPE:
                continue

            expected_type = self.TokenType.ARGUMENT_TYPE
            for i in range(index, len(self.tokenized)):
                in_token = self.tokenized[i]

                if expected_type == self.TokenType.ARGUMENT_NAME and in_token.type == self.TokenType.TYPE_UNION_SIGN:
                    expected_type = self.TokenType.ARGUMENT_TYPE
                    continue

                if in_token.type != expected_type:
                    raise SignatureTokenizerError(
                        f'Expected {expected_type}, got {in_token.type}. Function signature: \n' + self.code
                    )

                if expected_type == self.TokenType.ARGUMENT_TYPE:
                    expected_type = self.TokenType.ARGUMENT_NAME
                else:
                    break

    def tokenize(self) -> List['SignatureTokenizer.Token']:
        """
        Tokenization process
        :return: List of tokens
        """

        split_list = self.split()
        self.fill_tokenize(split_list)
        self.brackets_check(exception=False)

        self.function_name_and_returns_tokenize()
        self.default_value_tokenize()
        self.arguments_tokenize()
        self.concat_neighbours_tokenize()

        self.final_check()

        return self.tokenized


class SignatureParser:
    def __init__(self, tokenized: List[SignatureTokenizer.Token]):
        self.tokenized: List[SignatureTokenizer.Token] = tokenized

    def parse(self) -> FunctionType:
        pass
