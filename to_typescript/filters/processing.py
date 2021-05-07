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

            # Something like blacklist workaround
            if url.category.lower() in {
                'utf8 library',
            }:
                self.context.functions.pop(index)
                continue

            index += 1

    def prepare_argument_names(self):
        """
        Cleans the argument names from forbidden characters
        """
        for function in self.context.functions:
            for side, data in function:
                signature: FunctionSignature = data.signature

                # TODO: move into a separate method
                for argument_list in signature.arguments.arguments:
                    for argument in argument_list:
                        name = argument.name
                        if name:

                            # PROCESSING HERE
                            if name == 'var':
                                argument.name = 'variable'
                            if '/' in name:
                                argument.name = argument.name.replace('/', '_')

    def prepare_types(self):
        """
        Convert types
        """
        for function in self.context.functions:
            for side, data in function:
                signature: FunctionSignature = data.signature

                # TODO: move into a separate method
                for argument_list in signature.arguments.arguments:
                    for argument in argument_list:
                        types = argument.argument_type
                        if types:
                            types.names = [TypeConverter(name).convert() for name in types.names]

                for return_type in signature.return_types.return_types:
                    return_type.names = [TypeConverter(name).convert() for name in return_type.names]

    def resolve_multiple_signatures(self):
        """
        Example: export function fun(a?: int, b: int): int;
        Will be splitted into
        export function fun(a: int, b: int): int; // and
        export function fun(b: int): int;
        """
        for function in self.context.functions:
            for side, data in function:
                signature: FunctionSignature = data.signature

                # TODO: move into a separate method
                for argument_list in signature.arguments.arguments:
                    for argument in argument_list:
                        types = argument.argument_type
                        if types:
                            types.names = [TypeConverter(name).convert() for name in types.names]

                for return_type in signature.return_types.return_types:
                    # TODO: save the first optional and check is the current optional
                    # If not => copy current signature, remove args and insert after
                    # In the current make the optional args required
                    pass

    def apply(self):
        self._debug_only_element_section()

        self.prepare_argument_names()
        self.prepare_types()

        self.resolve_multiple_signatures()
