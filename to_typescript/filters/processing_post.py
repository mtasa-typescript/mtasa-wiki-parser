import enum
from typing import List, Tuple

from crawler.core.types import ListType as ListTypeOneSide
from to_python.core.types import FunctionData, FunctionGeneric, FunctionArgument, CompoundFunctionData
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


def get_functions_from_list_by_name(f_list: List[CompoundFunctionData],
                                    function_type: ListType,
                                    function_name: str) -> List[Tuple[CompoundFunctionData, ListTypeOneSide]]:
    """
    Gets function data list
    """
    if function_type == ListType.SHARED:
        return (
                get_functions_from_list_by_name(f_list,
                                                ListType.SERVER,
                                                function_name)
                + get_functions_from_list_by_name(f_list,
                                                  ListType.CLIENT,
                                                  function_name)
        )

    function_type_original = function_type.normalize()
    return [
        (f, function_type_original)
        for f in f_list
        if f[function_type_original] and f[function_type_original][0].name == function_name
    ]


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
        return [
            data[0][data[1]]
            for data in get_functions_from_list_by_name(self.context.functions, function_type, function_name)
        ]

    @staticmethod
    def iter_functions_arg_groups(functions: List[List[FunctionData]]):
        for function in functions:
            for declaration in function:
                for arg_group in declaration.signature.arguments.arguments:
                    yield arg_group

    def get_signature_arguments_by_name(self,
                                        functions: List[List[FunctionData]],
                                        argument_name: str) -> List[List[FunctionArgument]]:
        """
        Returns arguments by name
        :param functions: Function list
        :param argument_name: Name of the target argument
        """
        result: List[List[FunctionArgument]] = []
        for arg_group in self.iter_functions_arg_groups(functions):
            for arg in arg_group:
                if arg.name != argument_name:
                    continue

                result.append(arg_group)

        return result

    def replace_signature_argument(self,
                                   functions: List[List[FunctionData]],
                                   argument_name: str,
                                   new_function_argument: List[FunctionArgument]):
        """
        Replaces argument type
        :param functions: Function list
        :param argument_name: Name of the target argument
        :param new_function_argument: New function argument object
        """
        arguments = self.get_signature_arguments_by_name(
            functions,
            argument_name
        )
        if not arguments:
            raise FilterDumpProcessPostError(f'No arguments found.\n'
                                             f'Argument: {argument_name}')

        for arg_group in arguments:
            for arg in arg_group:
                if arg.name != argument_name:
                    continue

                arg_group[:] = new_function_argument  # Replace the whole list
                break

    def set_signature_variable_length(self,
                                      functions: List[List[FunctionData]],
                                      variable_length: bool):
        """
        Replaces argument type
        :param functions: Function list
        :param variable_length: Is there a variable arguments
        """
        for function in functions:
            for declaration in function:
                if variable_length is not None:
                    declaration.signature.arguments.variable_length = variable_length

    def add_signature_argument(self,
                               functions: List[List[FunctionData]],
                               new_function_argument: List[FunctionArgument]):
        for function in functions:
            for declaration in function:
                declaration.signature.arguments.arguments.append(new_function_argument)

    def remove_signature_argument(self,
                                  function_type: ListType,
                                  functions: List[List[FunctionData]],
                                  argument_name: str):
        """
        Removes argument by name
         :param function_type: SERVER / CLIENT
        :param function_name: Function Name
        :param argument_name: Name of the argument to be removed
        """
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
                                             f'Side: {function_type}, argument: {argument_name}')

    def add_generic_type(self, functions: List[List[FunctionData]], generic: FunctionGeneric):
        """
        Adds generic type into the function
        :param function_type: SERVER / CLIENT
        :param functions: List of function lists
        :param generic: Generic type info
        """
        for function in functions:
            for declaration in function:
                declaration.signature.generic_types.append(generic)

    def callback_functions(self):
        """
        Provides typing for callback functions
        """
        from to_typescript.function_post_config import apply_post_process
        apply_post_process(self)

    def callback_mixins(self):
        """
        Provides mixins
        """
        from to_typescript.mixins.oop_mixins import mixin_oop
        from to_typescript.mixins.function_mixins import mixin_function
        mixin_oop(self.context.oops)
        mixin_function(self.context.functions)

    def apply(self):
        """
        Applies post processing
        """
        self.callback_functions()
        self.callback_mixins()
        print('\u001b[32mPost processing complete\u001b[0m')
