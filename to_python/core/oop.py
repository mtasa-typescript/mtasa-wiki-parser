import enum
import re
from dataclasses import dataclass
from typing import List, Any, Dict

from to_python.core.signature import SignatureTokenizer
from to_python.core.types import FunctionOOP


class OOPTokenizerError(RuntimeError):
    pass


class OOPParserError(RuntimeError):
    pass


class OOPTokenizer:
    """
    Tokenizes an OOP definition
    """

    CHARS_TO_SPLIT = re.compile(r'([|]|\}\}|\{\{|\[\[|\]\])')

    def __init__(self, code: str):
        self.code = code
        self.tokenized: List[OOPTokenizer.Token] = []

    class TokenType(enum.Enum):
        START = 'Begin'
        END = 'End'
        DELIMITER = 'Delimiter'
        UNUSED = 'Unused'
        REFERENCE_START = 'ReferenceStart'
        REFERENCE_BODY = 'ReferenceBody'
        REFERENCE_END = 'ReferenceEnd'
        NOTE = 'Note'
        METHOD = 'Method'
        FIELD = 'Field'
        COUNTERPART_METHOD = 'CounterpartMethod'
        UNDEFINED = 'Undefined'

        def __repr__(self) -> str:
            return str(self)

    @dataclass
    class Token:
        type: 'OOPTokenizer.TokenType'
        value: str

    def fill_tokenize(self, split_list: List[str]):
        """
        Initializes self.tokenized. Determines obvious tokens.
        """
        for token in split_list:
            token_type = self.TokenType.UNDEFINED
            if token == '{{':
                token_type = self.TokenType.START
            elif token == '}}':
                token_type = self.TokenType.END
            if token == '[[':
                token_type = self.TokenType.REFERENCE_START
            elif token == ']]':
                token_type = self.TokenType.REFERENCE_END
            elif token == '|':
                token_type = self.TokenType.DELIMITER

            self.tokenized.append(self.Token(value=token,
                                             type=token_type))

    def references_tokenize(self):
        """
        Make everything inside reference brackets and braces a reference or an undefined
        Example: [[something|somethingelse]]
        """
        bracket_counter = 0
        for index, token in enumerate(self.tokenized):
            if token.type == self.TokenType.REFERENCE_START:
                bracket_counter += 1
                continue
            if token.type == self.TokenType.REFERENCE_END:
                bracket_counter -= 1
                continue

            if bracket_counter > 0:
                token.type = self.TokenType.REFERENCE_BODY
                continue

        bracket_counter = -1
        for index, token in enumerate(self.tokenized):
            if token.type == self.TokenType.START:
                if bracket_counter >= 0:
                    token.type = self.TokenType.UNDEFINED
                bracket_counter += 1
                continue
            if token.type == self.TokenType.END:
                bracket_counter -= 1
                if bracket_counter >= 0:
                    token.type = self.TokenType.UNDEFINED
                continue

            if bracket_counter > 0:
                token.type = self.TokenType.UNDEFINED
                continue

    def delimiters_check(self):
        """
        Expected 4 delimiters
        """
        counter = 0
        for token in self.tokenized:
            if token.type == self.TokenType.DELIMITER:
                counter += 1

        if counter > 5:
            raise OOPTokenizerError(f'Expected less than 5 delimiters, got {counter}. Code:\n{self.code}')

    def content_tokenize(self):
        """
        Apply tokens to content between the delimiters
        """
        index = 0
        delimiter_counter = 0

        counter_to_type = {
            0: self.TokenType.UNUSED,
            1: self.TokenType.NOTE,
            2: self.TokenType.METHOD,
            3: self.TokenType.FIELD,
            4: self.TokenType.COUNTERPART_METHOD,
        }

        skip = {
            self.TokenType.START,
            self.TokenType.END,
        }

        while index < len(self.tokenized):
            token = self.tokenized[index]
            if token.type in skip:
                index += 1
                continue

            elif token.type == self.TokenType.DELIMITER:
                delimiter_counter += 1

            else:
                token.type = counter_to_type[delimiter_counter]

            index += 1

    def final_check(self):
        """
        Check: there should be no UNDEFINED tokens
        """

        # No UNDEFINED Tokens
        for index, token in enumerate(self.tokenized):
            if token.type != self.TokenType.UNDEFINED:
                continue
            raise OOPTokenizerError('Undefined token. Function signature: \n' + self.code)

    def tokenize(self):
        """
        Tokenization
        :return:
        """
        split_list = SignatureTokenizer.split(self.code, self.CHARS_TO_SPLIT)
        self.fill_tokenize(split_list)
        self.references_tokenize()
        self.content_tokenize()

        self.delimiters_check()
        self.final_check()
        SignatureTokenizer.concat_neighbours_tokenize(tokenized=self.tokenized,
                                                      allowed={
                                                          self.TokenType.UNUSED,
                                                          self.TokenType.NOTE,
                                                          self.TokenType.METHOD,
                                                          self.TokenType.FIELD,
                                                          self.TokenType.COUNTERPART_METHOD,
                                                      })

        return self.tokenized


class OOPParser:
    """
    Parses an OOP definition into FunctionOOP
    """

    TokenType = OOPTokenizer.TokenType

    def __init__(self, tokenized: List[SignatureTokenizer.Token]):
        self.tokenized: List[SignatureTokenizer.Token] = tokenized

    @staticmethod
    def clean_method(code: str) -> str:
        code = re.sub(r'(\[\[|\]\])', '', code)
        return code.strip()

    @staticmethod
    def parse_method(text: str) -> Dict[str, Any]:
        """
        Selects method data
        :param text:
        :return:
        """
        text = OOPParser.clean_method(text)

        match = re.match(r'(.+)[.:](.+)', text)
        if match is None:
            if not text:
                raise OOPParserError(f'Wrong method content: {text}')

            return dict(class_name=text,
                        method_name=None,
                        is_static=True)

        return dict(class_name=match.group(1),
                    method_name=match.group(2),
                    is_static='.' in text, )

    def parse(self) -> FunctionOOP:
        misc_description = None
        field_name = None
        method_data = dict(
            class_name=None,
            method_name=None,
            is_static=None,
        )

        for token in self.tokenized:
            if token.type == self.TokenType.NOTE:
                misc_description = token.value
            elif token.type == self.TokenType.FIELD:
                field_name = token.value
            elif token.type == self.TokenType.METHOD:
                method_data = self.parse_method(token.value)

        return FunctionOOP(description=misc_description,
                           field=field_name,
                           **method_data)
