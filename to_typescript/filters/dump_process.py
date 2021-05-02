from to_python.core.types import FunctionSignature
from to_typescript.core.filter import FilterAbstract
from to_typescript.core.transform.extra_rules import TypeConverter


class FilterDumpProcess(FilterAbstract):
    """
    Post processing for dumps.
    Argument types changes, custom types, names, argument names, return types
    or additional information can be provided here
    """

    def _debug_only_element_section(self):
        index = 0
        while index < len(self.context.functions):
            f = self.context.functions[index]
            url = self.context.urls[(f.server or f.client).name]

            if 'element' not in url.category.lower():
                self.context.functions.pop(index)
                continue

            index += 1

    def prepare_types(self):
        """
        Convert types
        """
        for function in self.context.functions:
            for side, data in function:
                signature: FunctionSignature = data.signature

                for argument_list in signature.arguments.arguments:
                    for argument in argument_list:
                        types = argument.argument_type
                        types.names = [TypeConverter(name).convert() for name in types.names]

                for return_type in signature.return_types.return_types:
                    return_type.names = [TypeConverter(name).convert() for name in return_type.names]

    def apply(self):
        self._debug_only_element_section()
        self.prepare_types()
