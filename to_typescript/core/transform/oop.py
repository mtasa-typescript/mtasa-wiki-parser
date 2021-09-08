from copy import deepcopy
from typing import Optional

from crawler.core.types import PageUrl
from to_python.core.types import FunctionOOP, FunctionReturnTypes
from to_typescript.core.transform.function import TypeScriptFunctionGenerator


class TypeScriptOOPGeneratorError(RuntimeError):
    pass


class TypeScriptOOPGenerator:
    """
    Generates TypeScript function with JSDoc comments
    """

    MAX_DOC_LINE_LENGTH = 90

    def __init__(self, data: FunctionOOP, url: PageUrl, host_name: str):
        self.data = deepcopy(data)
        self.url = url
        self.host_name = host_name
        self.generator = TypeScriptFunctionGenerator(data.method, self.url,
                                                     self.host_name)

    def generate_field(self) -> Optional[str]:
        """
        Generates field
        """
        if self.data.field is None:
            return None

        static = ''
        if self.data.is_static:
            static = 'static '

        doc = f'''/**{self.generator.generate_doc_description(self.data.method.docs)}
 */'''

        return_type_static = self.generator.generate_return_type_static(
            FunctionReturnTypes(
                return_types=self.data.field.types,
                variable_length=False,
            )
        )
        return (
            f'{doc}\n'
            f'{static}{self.data.field.name}: '
            f'{return_type_static};'
        )

    def generate_method(self) -> Optional[str]:
        """
        Generates method
        """
        if self.data.method.name is None:
            return None

        args = TypeScriptFunctionGenerator.generate_arguments(
            self.generator.data.signature.arguments)
        args_brackets = f'''(
    {args}
)'''
        if not args:
            args_brackets = '()'

        static = ''
        if self.data.is_static:
            static = 'static '

        return_type = f': {self.generator.generate_return_type()}'
        if self.data.method.name == 'constructor':
            return_type = ''

        generics = TypeScriptFunctionGenerator.generate_generics(
            self.data.method.signature.generic_types)
        if self.data.method.name == 'constructor':
            generics = ''

        return f'''/**{self.generator.generate_doc()} */
{static}{self.data.method.name}{generics}{args_brackets}{return_type};'''
