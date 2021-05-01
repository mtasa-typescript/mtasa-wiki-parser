from typing import List

from crawler.core.types import FunctionUrl
from to_python.core.types import FunctionData, FunctionType, FunctionArgument
from to_typescript.core.transform.extra_rules import TypeConverter


class TypeScriptFunctionGeneratorError(RuntimeError):
    pass


class TypeScriptFunctionGenerator:
    """
    Generates TypeScript function with JSDoc comments
    """

    MAX_DOC_LINE_LENGTH = 90

    def __init__(self, data: FunctionData, url: FunctionUrl, host_name: str):
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

                add_line = line[index_to_cut:]
                lines[index] = line[:index_to_cut]
                lines.insert(index + 1, add_line)

            index += 1

        return '\n * '.join(lines)

    def generate_doc(self) -> str:
        """
        Generates JSDoc
        """
        docs = self.data.docs

        doc_param_list = []
        for arg_name in docs.arguments:
            arg_desc = docs.arguments[arg_name]
            doc_param_list.append(f' * @param {arg_name} {self.cut_doc_lines(arg_desc)}')
        doc_params = '\n'.join(doc_param_list)
        doc_params += '\n' if doc_param_list else ''

        doc_return = self.cut_doc_lines(docs.result)
        doc_return = f' * @return {doc_return}\n' if doc_return else ''

        # TODO: Add @default
        result = f'''/**
 * {self.cut_doc_lines(docs.description)}
 * @see {{@link {self.host_name}{self.url.url} | Wiki, {self.url.name} }}
{doc_params}{doc_return} */'''

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

        # Multiple
        if signature.return_types.variable_length or len(signature.return_types.return_types) > 1:
            result = 'LuaMultiReturn<[\n'
            result += ',\n'.join('    ' + self.function_type_text(t)
                                 for t in signature.return_types.return_types)

            if signature.return_types.variable_length:
                if len(signature.return_types.return_types) > 1:
                    result += ',\n'
                result += '    ' + '...any[]\n'
            return result + ']>'

        # Nothing
        if not signature.return_types.return_types:
            return 'void'

        # Single
        return self.function_type_text(signature.return_types.return_types[0])

    @staticmethod
    def function_arg_text(arg: List[FunctionArgument]) -> str:
        """
        Converts a single argument
        """
        type_names = []
        for a in arg:
            type_names.extend(a.argument_type.names)

        name = arg[0].name
        if arg[0].argument_type.is_optional:
            name += '?'

        type_str = ' | '.join(type_names)
        return f'{name}: {type_str}'

    def generate_arguments(self) -> str:
        """
        Generates TypeScript function arguments
        """
        arguments = self.data.signature.arguments
        arg_list = arguments.arguments.copy()

        postfix = ''

        if arguments.variable_length:
            if len(arg_list[-1]) > 1:
                raise TypeScriptFunctionGeneratorError(
                    'Varargs: Cannot transpile multiple arguments at the last position')

            last_arg = arg_list[-1][0]
            if TypeConverter.is_varargs_type(last_arg.argument_type):
                arg_list.pop(-1)
            postfix = '...varargs: any[]'

        args = []
        for arg in arg_list:
            args.append(self.function_arg_text(arg))

        if postfix:
            args.append(postfix)

        return ',\n    '.join(args)

    def generate(self) -> str:
        pass
