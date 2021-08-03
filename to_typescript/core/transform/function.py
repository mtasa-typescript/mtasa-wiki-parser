from copy import copy
from typing import List

from crawler.core.types import PageUrl
from to_python.core.types import FunctionData, FunctionType, FunctionArgument, FunctionDoc, FunctionGeneric, \
    FunctionArgumentValues
from to_typescript.core.transform.extra_rules import is_varargs_type


class TypeScriptFunctionGeneratorError(RuntimeError):
    pass


class TypeScriptFunctionGenerator:
    """
    Generates TypeScript function with JSDoc comments
    """

    MAX_DOC_LINE_LENGTH = 90

    def __init__(self, data: FunctionData, url: PageUrl, host_name: str):
        self.data = data
        self.url = url
        self.host_name = host_name

    @staticmethod
    def cut_doc_lines(text: str) -> str:
        """
        Cuts lines with length more than 80 chars
        """
        lines = text.split('\n')

        index = 0
        while index < len(lines):
            lines[index] = lines[index].strip()
            line = lines[index].strip()

            if line == '':
                lines.pop(index)
                continue

            if len(line) > TypeScriptFunctionGenerator.MAX_DOC_LINE_LENGTH:
                index_to_cut = TypeScriptFunctionGenerator.MAX_DOC_LINE_LENGTH
                for i in range(TypeScriptFunctionGenerator.MAX_DOC_LINE_LENGTH):
                    if line[i] == ' ':
                        index_to_cut = i

                add_line = line[index_to_cut:].strip()
                lines[index] = line[:index_to_cut].strip()
                lines.insert(index + 1, add_line)

            index += 1

        return '\n * '.join(lines)

    @staticmethod
    def generate_doc_description(docs: FunctionDoc) -> str:
        """
        Generates JSDoc function description
        """
        description = TypeScriptFunctionGenerator.cut_doc_lines(docs.description)

        if not description:
            return ''

        return f'\n * {description}'

    def generate_doc(self) -> str:
        """
        Generates JSDoc
        """
        docs = self.data.docs

        doc_description = self.generate_doc_description(docs)

        doc_param_list = []
        for arg_name in docs.arguments:
            arg_desc = docs.arguments[arg_name]
            doc_param_list.append(f' * @param {arg_name} {self.cut_doc_lines(arg_desc)}'.rstrip())

        doc_params = '\n'.join(doc_param_list)
        doc_params += '\n' if doc_param_list else ''

        doc_return = self.cut_doc_lines(docs.result)
        doc_return = f' * @return {doc_return}\n' if doc_return else ''

        # TODO: Add @default
        result = f'''{doc_description}
 * @see {self.host_name}{self.url.url}
{doc_params}{doc_return}'''

        return result

    @staticmethod
    def function_type_text(t: FunctionType) -> str:
        names = t.names.copy()
        if t.is_optional:
            names.append('undefined')

        return ' | '.join(names)

    def generate_return_type(self) -> str:
        """
        Generates return TypeScript type
        """
        signature = self.data.signature
        return_types = copy(signature.return_types.return_types)

        # Multiple
        if signature.return_types.variable_length or len(return_types) > 1:
            last_arg = return_types[-1]
            if is_varargs_type(last_arg):
                return_types.pop(-1)

            result = 'LuaMultiReturn<[\n'
            result += ',\n'.join('    ' + self.function_type_text(t)
                                 for t in return_types)

            if signature.return_types.variable_length:
                if len(return_types) > 1:
                    result += ',\n'
                result += '    ' + '...any[]'
            return result + '\n]>'

        # Nothing
        if not signature.return_types.return_types:
            return 'void'

        # Single
        return self.function_type_text(return_types[0])

    @staticmethod
    def function_arg_text(arg: List[FunctionArgument]) -> str:
        """
        Converts a single argument
        """
        type_names = []
        for a in arg:
            if a.argument_type is None:
                raise TypeScriptFunctionGeneratorError(f'No type information for argument "{a.name}"')

            type_names.extend(a.argument_type.names)

        name = arg[0].name
        if arg[0].argument_type.is_optional:
            name += '?'

        type_str = ' | '.join(type_names)
        return f'{name}: {type_str}'

    @staticmethod
    def generate_arguments(arguments: FunctionArgumentValues) -> str:
        """
        Generates TypeScript function arguments
        """
        arg_list = arguments.arguments.copy()

        postfix = ''

        if arguments.variable_length:
            if len(arg_list[-1]) > 1:
                raise TypeScriptFunctionGeneratorError(
                    'Varargs: Cannot transpile multiple arguments at the last position')

            last_arg = arg_list[-1][0]
            if is_varargs_type(last_arg.argument_type):
                arg_list.pop(-1)
            postfix = '...varargs: any[]'

        args = []
        for arg in arg_list:
            args.append(TypeScriptFunctionGenerator.function_arg_text(arg))

        if postfix:
            args.append(postfix)

        return ',\n    '.join(args)

    @staticmethod
    def generate_generics(generics: List[FunctionGeneric]) -> str:
        """
        Generates generics declarations
        """
        if not generics:
            return ''

        generic_strs = []
        for generic in generics:
            string = generic.name
            if generic.extends:
                string += f' extends {generic.extends}'

            if generic.default_value:
                string += f' = {generic.default_value}'

            generic_strs.append(string)

        result = '<\n    '
        result += ',\n    '.join(generic_strs)
        return result + '\n>'

    def generate(self) -> str:
        """
        Generates function declaration
        """
        args = self.generate_arguments(self.data.signature.arguments)
        args_brackets = f'''(
    {args}
)'''
        if not args:
            args_brackets = '()'

        generics = self.generate_generics(self.data.signature.generic_types)

        return f'''/**{self.generate_doc()} * @noSelf
 */
export declare function {self.data.name}{generics}{args_brackets}: {self.generate_return_type()};'''
