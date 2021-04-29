import enum
import re
import sys
from dataclasses import dataclass
from typing import Optional, List

from wikitextparser import WikiText

from to_python.core.context import ParseFunctionSide
from to_python.core.filter import FilterAbstract
from to_python.core.types import FunctionType
from to_python.filters.data_list.doc import FilterParseDocs


class SignatureParserError(RuntimeError):
    pass


class SignatureParser:
    CHARS_TO_SPLIT = re.compile(r'[(\[\]=,) ]')

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

    @dataclass
    class Token:
        type: 'SignatureParser.TokenType'
        value: str

    def __init__(self, code: str):
        self.code = code
        self.tokenized: List[SignatureParser.Token] = []

    def token_should_be_undefined(self, token: 'SignatureParser.Token'):
        if token.type != self.TokenType.UNDEFINED:
            raise SignatureParserError(f'Expected UNDEFINED token, got {str(token.type)}. '
                                       f'Function signature:\n{self.code}')

    def tokenize(self):
        """
        Fills self.tokenized
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
        split = list(filter(lambda x: x != '' and x != ' ', split))

        # Fills
        for token in split:
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

            self.tokenized.append(self.Token(value=token,
                                             type=token_type))

        # Determine function name and return types
        for index, token in enumerate(self.tokenized):
            if token.type != self.TokenType.ARGUMENT_START:
                continue

            self.token_should_be_undefined(self.tokenized[index - 1])
            self.tokenized[index - 1].type = self.TokenType.FUNCTION_NAME
            for i in range(0, index - 1):
                self.token_should_be_undefined(self.tokenized[i])
                self.tokenized[i].type = self.TokenType.RETURN_TYPE

            break

        # After equal sign there is always a default value
        for index, token in enumerate(self.tokenized):
            if token.type != self.TokenType.EQUAL_SIGN:
                continue
            self.token_should_be_undefined(self.tokenized[index + 1])
            self.tokenized[index + 1].type = self.TokenType.DEFAULT_VALUE

        # After comma sign expected: [optional start/optional end] + type + argument name
        for index, token in enumerate(self.tokenized):
            if token.type not in {self.TokenType.COMMA_SIGN, self.TokenType.ARGUMENT_START}:
                continue

            current_type = self.TokenType.ARGUMENT_TYPE
            for i in range(index + 1, len(self.tokenized)):
                in_token = self.tokenized[i]
                if in_token.type in {self.TokenType.OPTIONAL_START, self.TokenType.OPTIONAL_END}:
                    continue
                if in_token.type in {self.TokenType.COMMA_SIGN}:
                    break

                self.token_should_be_undefined(self.tokenized[i])
                self.tokenized[i].type = current_type

                if current_type == self.TokenType.ARGUMENT_TYPE:
                    current_type = self.TokenType.ARGUMENT_NAME
                else:
                    break

        # In the end there should be no UNDEFINED tokens
        for index, token in enumerate(self.tokenized):
            if token.type != self.TokenType.UNDEFINED:
                continue
            raise RuntimeError('Undefined token. Function signature: \n' + self.code)

    def parse(self) -> FunctionType:
        self.tokenize()


class FilterParseFunctionSignature(FilterAbstract):
    """
    Parses function signature
    """

    @staticmethod
    def clean_code(code: str) -> str:
        lines = code.split('\n')
        for i, line in enumerate(lines):
            line = re.sub(r'--.+$', '', line)

            lines[i] = line.strip()

        return ' '.join(lines)

    def parse_signature(self, code: str) -> FunctionType:
        """
        Parses given code
        """
        code = self.clean_code(code)

        SignatureParser(code).parse()
        print(code)

    def pick_signature_container(self, f_name: str, raw_data: str, wiki: WikiText) -> str:
        """
        Picks media wiki code, containing signature
        """
        syntax = FilterParseDocs.get_sections_title_contains(wiki, 'syntax')
        if not syntax:
            if self.context.side_data[f_name].side != ParseFunctionSide.SHARED:
                print(f'[WARN] No Syntax section "{f_name}"', file=sys.stderr)
            syntax_index = 0
            start_index = 0

        else:
            if len(syntax) != 1:
                print(f'[WARN] Multiple Syntax sections "{f_name}". \n[WARN] Selecting the first:', file=sys.stderr)
                for section, index in syntax:
                    print(f'    {index: 2}. {section.title}', file=sys.stderr)

            syntax, syntax_index = syntax[0]
            start_index = syntax.span[0]

        try:
            next_section: Optional[WikiText] = wiki.sections[syntax_index + 1]
        except IndexError:
            next_section = None

        if next_section is None:
            end_index = len(str(wiki))
        else:
            end_index = next_section.span[0]

        code_inside = str(wiki)[start_index:end_index]
        if 'syntaxhighlight' not in code_inside:
            raise RuntimeError(f'[ERROR] Result media wiki code does not contain signature. "{f_name}"')

        return code_inside

    SELECT_CODE_REGEX = re.compile(r'<syntaxhighlight[^>]*>([\s\S]+?)</syntaxhighlight>')

    def pick_signature(self, f_name: str, raw_data: str, wiki: WikiText) -> str:
        """
        Picks out function signature code from an entire data
        """
        container = self.pick_signature_container(f_name, raw_data, wiki)
        signature = re.search(self.SELECT_CODE_REGEX, container).group(1)
        return signature.strip()

    def apply(self):
        for f_name in self.context.parsed:
            raw_content = self.context.side_data[f_name]
            wiki_content = self.context.wiki_side[f_name]

            if raw_content.client is not None:
                self.context.parsed[f_name].client.signature = self.parse_signature(
                    self.pick_signature(f_name, raw_content.client, wiki_content.client)
                )

            if raw_content.server is not None:
                self.context.parsed[f_name].server.signature = self.parse_signature(
                    self.pick_signature(f_name, raw_content.server, wiki_content.server)
                )
