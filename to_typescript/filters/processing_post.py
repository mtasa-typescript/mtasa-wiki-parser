import enum
from typing import List

from crawler.core.types import ListType as ListTypeOneSide
from to_python.core.types import FunctionData, FunctionGeneric, FunctionArgument
from to_typescript.core.filter import FilterAbstract


class FilterDumpProcessPostError(RuntimeError):
    pass


class ListType(enum.Enum):
    CLIENT = 'Client'
    SERVER = 'Server'
    SHARED = 'Shared'

    def normalize(self) -> ListTypeOneSide:
        if self == self.CLIENT:
            return ListTypeOneSide.CLIENT
        if self == self.SERVER:
            return ListTypeOneSide.SERVER


class FilterDumpProcessPost(FilterAbstract):
    """
    Post-post processing for dumps.
    Any additional information or definitions can be provided here
    """

    def get_functions(self,
                      function_type: ListType,
                      function_name: str) -> List[List[FunctionData]]:
        """
        Gets function data list
        :param function_type:
        :param function_name:
        :return:
        """
        if function_type == ListType.SHARED:
            return (
                    self.get_functions(ListType.SERVER, function_name)
                    + self.get_functions(ListType.CLIENT, function_name)
            )

        function_type_original = function_type.normalize()
        return list(map(
            lambda f: f[function_type_original],
            filter(
                lambda f: f[function_type_original] and f[function_type_original][0].name == function_name,
                self.context.functions,
            )
        ))

    @staticmethod
    def iter_functions_arg_groups(functions: List[List[FunctionData]]):
        for function in functions:
            for declaration in function:
                for arg_group in declaration.signature.arguments.arguments:
                    yield arg_group

    def get_signature_arguments_by_name(self,
                                        function_type: ListType,
                                        function_name: str,
                                        argument_name: str) -> List[List[FunctionArgument]]:
        """
        Returns arguments by name
        :param function_type: SERVER / CLIENT
        :param function_name: Function Name
        :param argument_name: Name of the target argument
        """
        functions = self.get_functions(function_type, function_name)
        if not functions:
            raise FilterDumpProcessPostError(f'No such function: "{function_type}", "{function_name}"')

        result: List[List[FunctionArgument]] = []
        for arg_group in self.iter_functions_arg_groups(functions):
            for arg in arg_group:
                if arg.name != argument_name:
                    continue

                result.append(arg_group)

        return result

    def replace_signature_argument(self,
                                   function_type: ListType,
                                   function_name: str,
                                   argument_name: str,
                                   new_function_argument: List[FunctionArgument]):
        """
        Replaces argument type
        :param function_type: SERVER / CLIENT
        :param function_name: Function Name
        :param argument_name: Name of the target argument
        :param new_function_argument: New function argument object
        """
        arguments = self.get_signature_arguments_by_name(
            function_type,
            function_name,
            argument_name
        )
        if not arguments:
            raise FilterDumpProcessPostError(f'No arguments found.\n'
                                             f'Side: {function_type}, name: {function_name}, argument: {argument_name}')

        for arg_group in arguments:
            for arg in arg_group:
                if arg.name != argument_name:
                    continue

                arg_group[:] = new_function_argument  # Replace the whole list
                break

    def set_signature_variable_length(self,
                                      function_type: ListType,
                                      function_name: str,
                                      variable_length: bool):
        """
        Replaces argument type
        :param function_type: SERVER / CLIENT
        :param function_name: Function Name
        :param variable_length: Is there a variable arguments
        """
        functions = self.get_functions(function_type, function_name)
        if not functions:
            raise FilterDumpProcessPostError(f'No such function: "{function_type}", "{function_name}"')

        for function in functions:
            for declaration in function:
                if variable_length is not None:
                    declaration.signature.arguments.variable_length = variable_length

    def add_signature_argument(self,
                               function_type: ListType,
                               function_name: str,
                               new_function_argument: List[FunctionArgument]):
        functions = self.get_functions(function_type, function_name)
        if not functions:
            raise FilterDumpProcessPostError(f'No such function: "{function_type}", "{function_name}"')

        for function in functions:
            for declaration in function:
                declaration.signature.arguments.arguments.append(new_function_argument)

    def remove_signature_argument(self,
                                  function_type: ListType,
                                  function_name: str,
                                  argument_name: str):
        """
        Removes argument by name
         :param function_type: SERVER / CLIENT
        :param function_name: Function Name
        :param argument_name: Name of the argument to be removed
        """
        functions = self.get_functions(function_type, function_name)
        if not functions:
            raise FilterDumpProcessPostError(f'No such function: "{function_type}", "{function_name}"')

        removed = 0
        for function in functions:
            for declaration in function:
                index = 0

                argument_list = declaration.signature.arguments.arguments
                while index < len(argument_list):
                    if argument_list[index][0].name == argument_name:
                        argument_list.pop(index)
                        removed += 1
                        continue

                    index += 1

        if not removed:
            raise FilterDumpProcessPostError(f'No arguments was removed.\n'
                                             f'Side: {function_type}, name: {function_name}, argument: {argument_name}')

    def add_generic_type(self, function_type: ListType, function_name: str, generic: FunctionGeneric):
        """
        Adds generic type into the function
        :param function_type: SERVER / CLIENT
        :param function_name: Name of the target function
        :param generic: Generic type info
        """
        functions = self.get_functions(function_type, function_name)
        if not functions:
            raise FilterDumpProcessPostError(f'No such function: "{function_type}", "{function_name}"')

        for function in functions:
            for declaration in function:
                declaration.signature.generic_types.append(generic)

    def callback_functions(self):
        """
        Provides typing for callback functions
        """
        from to_typescript.function_post_config import apply_post_process
        apply_post_process(self)

    def apply(self):
        """
        Applies post processing
        """
        self.callback_functions()
        print('\u001b[32mPost processing complete\u001b[0m')
