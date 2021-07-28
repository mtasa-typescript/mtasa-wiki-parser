import enum
from typing import List

from crawler.core.types import ListType as ListTypeOneSide
from to_python.core.types import FunctionData, FunctionGeneric, FunctionArgument, FunctionType
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
        functions = self.get_functions(function_type, function_name)
        if not functions:
            raise FilterDumpProcessPostError(f'No such function: "{function_type}", "{function_name}"')

        for function in functions:
            for declaration in function:
                for arg_group in declaration.signature.arguments.arguments:
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
        # TODO: throw an error, if there is no arguments with the specified name
        functions = self.get_functions(function_type, function_name)
        if not functions:
            raise FilterDumpProcessPostError(f'No such function: "{function_type}", "{function_name}"')

        for function in functions:
            for declaration in function:
                index = 0

                argument_list = declaration.signature.arguments.arguments
                while index < len(argument_list):
                    if argument_list[index][0].name == argument_name:
                        argument_list.pop(index)
                        continue

                    index += 1

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
        # TODO FIXME MOVE INTO SEPARATED FILE
        # TODO FIXME MOVE INTO SEPARATED FILE
        # TODO FIXME MOVE INTO SEPARATED FILE
        self.replace_signature_argument(
            ListType.SHARED,
            'fetchRemote',
            'callbackFunction',
            [FunctionArgument(
                name='callbackFunction',
                argument_type=FunctionType(
                    names=['FetchRemoteCallback'],
                    is_optional=False
                ),
                default_value=None,
            )]
        )

        self.replace_signature_argument(
            ListType.SHARED,
            'addEventHandler',
            'handlerFunction',
            [FunctionArgument(
                name='handlerFunction',
                argument_type=FunctionType(
                    names=['CallbackType["function"]'],
                    is_optional=False
                ),
                default_value=None,
            )]
        )
        self.replace_signature_argument(
            ListType.SHARED,
            'addEventHandler',
            'eventName',
            [FunctionArgument(
                name='eventName',
                argument_type=FunctionType(
                    names=['CallbackType["name"]'],
                    is_optional=False
                ),
                default_value=None,
            )]
        )
        self.add_generic_type(
            ListType.SHARED,
            'addEventHandler',
            FunctionGeneric(
                name='CallbackType',
                extends='GenericEventHandler',
                default_value='GenericEventHandler'
            )
        )

        self.replace_signature_argument(
            ListType.SHARED,
            'removeEventHandler',
            'eventName',
            [FunctionArgument(
                name='eventName',
                argument_type=FunctionType(
                    names=['CallbackType["name"]'],
                    is_optional=False
                ),
                default_value=None,
            )]
        )
        self.replace_signature_argument(
            ListType.SHARED,
            'removeEventHandler',
            'functionVar',
            [FunctionArgument(
                name='functionVar',
                argument_type=FunctionType(
                    names=['CallbackType["function"]'],
                    is_optional=False
                ),
                default_value=None,
            )]
        )

        self.add_generic_type(
            ListType.SHARED,
            'removeEventHandler',
            FunctionGeneric(
                name='CallbackType',
                extends='GenericEventHandler',
                default_value='GenericEventHandler'
            )
        )

        self.set_signature_variable_length(
            ListType.SHARED,
            'triggerEvent',
            False,
        )
        self.remove_signature_argument(
            ListType.SHARED,
            'triggerEvent',
            'argument1',
        )
        self.replace_signature_argument(
            ListType.SHARED,
            'triggerEvent',
            'eventName',
            [FunctionArgument(
                name='eventName',
                argument_type=FunctionType(
                    names=['CallbackType["name"]'],
                    is_optional=False
                ),
                default_value=None,
            )]
        )
        self.add_signature_argument(
            ListType.SHARED,
            'triggerEvent',
            [FunctionArgument(
                name='...args',
                argument_type=FunctionType(
                    names=['Parameters<CallbackType["function"]>'],
                    is_optional=False
                ),
                default_value=None,
            )]
        )
        self.add_generic_type(
            ListType.SHARED,
            'triggerEvent',
            FunctionGeneric(
                name='CallbackType',
                extends='GenericEventHandler',
                default_value='GenericEventHandler'
            )
        )

        self.set_signature_variable_length(
            ListType.CLIENT,
            'triggerLatentServerEvent',
            False,
        )
        self.remove_signature_argument(
            ListType.CLIENT,
            'triggerLatentServerEvent',
            'arguments',
        )
        self.replace_signature_argument(
            ListType.CLIENT,
            'triggerLatentServerEvent',
            'event',
            [FunctionArgument(
                name='event',
                argument_type=FunctionType(
                    names=['CallbackType["name"]'],
                    is_optional=False
                ),
                default_value=None,
            )]
        )
        self.add_signature_argument(
            ListType.CLIENT,
            'triggerLatentServerEvent',
            [FunctionArgument(
                name='...args',
                argument_type=FunctionType(
                    names=['Parameters<CallbackType["function"]>'],
                    is_optional=False
                ),
                default_value=None,
            )]
        )
        self.add_generic_type(
            ListType.CLIENT,
            'triggerLatentServerEvent',
            FunctionGeneric(
                name='CallbackType',
                extends='GenericEventHandler',
                default_value='GenericEventHandler'
            )
        )

        self.set_signature_variable_length(
            ListType.CLIENT,
            'triggerServerEvent',
            False,
        )
        self.remove_signature_argument(
            ListType.CLIENT,
            'triggerServerEvent',
            'arguments',
        )
        self.replace_signature_argument(
            ListType.CLIENT,
            'triggerServerEvent',
            'event',
            [FunctionArgument(
                name='event',
                argument_type=FunctionType(
                    names=['CallbackType["name"]'],
                    is_optional=False
                ),
                default_value=None,
            )]
        )
        self.add_signature_argument(
            ListType.CLIENT,
            'triggerServerEvent',
            [FunctionArgument(
                name='...args',
                argument_type=FunctionType(
                    names=['Parameters<CallbackType["function"]>'],
                    is_optional=False
                ),
                default_value=None,
            )]
        )
        self.add_generic_type(
            ListType.CLIENT,
            'triggerServerEvent',
            FunctionGeneric(
                name='CallbackType',
                extends='GenericEventHandler',
                default_value='GenericEventHandler'
            )
        )

        self.set_signature_variable_length(
            ListType.SERVER,
            'triggerLatentClientEvent',
            False,
        )
        self.remove_signature_argument(
            ListType.SERVER,
            'triggerLatentClientEvent',
            'arguments',
        )
        self.replace_signature_argument(
            ListType.SERVER,
            'triggerLatentClientEvent',
            'name',
            [FunctionArgument(
                name='name',
                argument_type=FunctionType(
                    names=['CallbackType["name"]'],
                    is_optional=False
                ),
                default_value=None,
            )]
        )
        self.add_signature_argument(
            ListType.SERVER,
            'triggerLatentClientEvent',
            [FunctionArgument(
                name='...args',
                argument_type=FunctionType(
                    names=['Parameters<CallbackType["function"]>'],
                    is_optional=False
                ),
                default_value=None,
            )]
        )
        self.add_generic_type(
            ListType.SERVER,
            'triggerLatentClientEvent',
            FunctionGeneric(
                name='CallbackType',
                extends='GenericEventHandler',
                default_value='GenericEventHandler'
            )
        )

        self.set_signature_variable_length(
            ListType.SERVER,
            'triggerClientEvent',
            False,
        )
        self.remove_signature_argument(
            ListType.SERVER,
            'triggerClientEvent',
            'arguments',
        )
        self.replace_signature_argument(
            ListType.SERVER,
            'triggerClientEvent',
            'name',
            [FunctionArgument(
                name='name',
                argument_type=FunctionType(
                    names=['CallbackType["name"]'],
                    is_optional=False
                ),
                default_value=None,
            )]
        )
        self.add_signature_argument(
            ListType.SERVER,
            'triggerClientEvent',
            [FunctionArgument(
                name='...args',
                argument_type=FunctionType(
                    names=['Parameters<CallbackType["function"]>'],
                    is_optional=False
                ),
                default_value=None,
            )]
        )
        self.add_generic_type(
            ListType.SERVER,
            'triggerClientEvent',
            FunctionGeneric(
                name='CallbackType',
                extends='GenericEventHandler',
                default_value='GenericEventHandler'
            )
        )

        self.replace_signature_argument(
            ListType.SHARED,
            'addCommandHandler',
            'handlerFunction',
            [FunctionArgument(
                name='handlerFunction',
                argument_type=FunctionType(
                    names=['CommandHandler'],
                    is_optional=False,
                ),
                default_value=None,
            )]
        )

    def apply(self):
        """
        Applies post processing
        """
        self.callback_functions()
