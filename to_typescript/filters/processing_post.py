from typing import List

from to_python.core.types import FunctionData
from to_typescript.core.filter import FilterAbstract


class FilterDumpProcessPost(FilterAbstract):
    """
    Post-post processing for dumps.
    Any additional information or definitions can be provided here
    """

    def replace_signature_type(self, function_name: str, argument_name: str, new_types: List[str]):
        """
        Replaces argument type
        :param function_name: Function Name
        :param argument_name: Name of the target argument
        :param new_type: Type to be replaced
        """
        for f in self.context.functions:
            name = (f.client or f.server)[0].name

            if name != function_name:
                continue

            for t, _ in f:
                for declaration in getattr(f, t):
                    declaration: FunctionData
                    # Oh shit
                    for arg_group in declaration.signature.arguments.arguments:
                        for arg in arg_group:
                            if arg.name != argument_name:
                                continue

                            arg.argument_type.names = new_types

    def callback_functions(self):
        """
        Provides typing for callback functions
        """
        self.replace_signature_type('fetchRemote', 'callbackFunction', ['FetchRemoteCallback'])

    def apply(self):
        """
        Applies post processing
        """
        self.callback_functions()
