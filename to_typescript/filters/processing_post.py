from typing import List

from crawler.core.types import ListType
from to_python.core.types import FunctionData, FunctionGeneric
from to_typescript.core.filter import FilterAbstract


class FilterDumpProcessPostError(RuntimeError):
    pass


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
        return list(map(
            lambda f: f[function_type],
            filter(
                lambda f: f[function_type] and f[function_type][0].name == function_name,
                self.context.functions,
            )
        ))

    def replace_signature_type(self,
                               function_type: ListType,
                               function_name: str,
                               argument_name: str,
                               new_types: List[str]):
        """
        Replaces argument type
        :param function_type: SERVER / CLIENT
        :param function_name: Function Name
        :param argument_name: Name of the target argument
        :param new_types: Types list to be replaced
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

                        arg.argument_type.names = new_types

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
        self.replace_signature_type(ListType.SERVER, 'fetchRemote', 'callbackFunction', ['FetchRemoteCallback'])
        self.replace_signature_type(ListType.CLIENT, 'fetchRemote', 'callbackFunction', ['FetchRemoteCallback'])

        self.replace_signature_type(ListType.SERVER, 'addEventHandler', 'handlerFunction', ['CallbackType["function"]'])
        self.replace_signature_type(ListType.CLIENT, 'addEventHandler', 'handlerFunction', ['CallbackType["function"]'])
        self.replace_signature_type(ListType.SERVER, 'addEventHandler', 'eventName', ['CallbackType["name"]'])
        self.replace_signature_type(ListType.CLIENT, 'addEventHandler', 'eventName', ['CallbackType["name"]'])
        self.add_generic_type(ListType.CLIENT, 'addEventHandler', FunctionGeneric(name='CallbackType',
                                                                                  extends='GenericEventHandler',
                                                                                  default_value='GenericEventHandler'))
        self.add_generic_type(ListType.SERVER, 'addEventHandler', FunctionGeneric(name='CallbackType',
                                                                                  extends='GenericEventHandler',
                                                                                  default_value='GenericEventHandler'))

    def apply(self):
        """
        Applies post processing
        """
        self.callback_functions()
