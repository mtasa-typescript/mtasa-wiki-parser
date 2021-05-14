from copy import copy
from typing import Optional

from crawler.core.types import FunctionUrl
from to_python.core.types import FunctionData
from to_typescript.core.transform.function import TypeScriptFunctionGenerator


class TypeScriptOOPGeneratorError(RuntimeError):
    pass


class TypeScriptOOPGenerator:
    """
    Generates TypeScript function with JSDoc comments
    """

    MAX_DOC_LINE_LENGTH = 90

    def __init__(self, data: FunctionData, url: FunctionUrl, host_name: str):
        self.data = copy(data)
        self.url = url
        self.host_name = host_name
        self.generator = TypeScriptFunctionGenerator(self.data, self.url, self.host_name)

        # Remove first argument, if method is not static
        if not self.data.oop.is_static:
            arguments = self.data.signature.arguments.arguments
            if arguments:
                arg_name = arguments[0][0].name
                name = arg_name
                if name in data.docs.arguments:
                    data.docs.arguments.pop(name)

                arguments.pop(0)

    def generate_field(self) -> Optional[str]:
        """
        Generates field
        """
        if self.data.oop.field is None:
            return None

        static = ''
        if self.data.oop.is_static:
            static = 'static '

        doc = f'''/**{self.generator.generate_doc_description(self.data.docs)}
 */'''
        return f'''{doc}
{static}{self.data.oop.field}: {self.generator.generate_return_type()};'''

    def generate_method(self) -> Optional[str]:
        """
        Generates method
        """
        if self.data.oop.method_name is None:
            return None

        args = self.generator.generate_arguments()
        args_brackets = f'''(
    {args}
)'''
        if not args:
            args_brackets = '()'

        static = ''
        if self.data.oop.is_static:
            static = 'static '

        return_type = f': {self.generator.generate_return_type()}'
        if self.data.oop.method_name == 'constructor':
            return_type = ''

        return f'''{self.generator.generate_doc()}
{static}{self.data.oop.method_name}{args_brackets}{return_type};'''
