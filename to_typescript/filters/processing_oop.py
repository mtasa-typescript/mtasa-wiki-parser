import re
from copy import deepcopy
from typing import List, Dict

from crawler.core.types import ListType
from to_python.core.types import \
    FunctionOOP, \
    FunctionData, \
    CompoundFunctionData
from to_typescript.core.filter import FilterAbstract
from to_typescript.core.transform.extra_rules import TypeConverter
from to_typescript.filters.processing_function import \
    FilterDumpProcessFunctions


class FilterDumpProcessOOP(FilterAbstract):
    """
    Post processing for dumps (OOP).
    Argument types changes, custom types, names, argument names, return types
    or additional information can be provided here
    """

    CLASS_NAME_SELECTOR = re.compile(r'^([^|]*\|(.+))$')

    def prepare_signature(self, data: FunctionOOP):
        white_list = {
            'element',
            'guielement',
        }

        if data.field:
            FilterDumpProcessFunctions.prepare_return_types(data.field.types)

        if data.method:
            FilterDumpProcessFunctions.prepare_return_types(
                data.method.signature.return_types.return_types
            )
            FilterDumpProcessFunctions.prepare_argument_names(
                data.method.signature.arguments.arguments
            )
            FilterDumpProcessFunctions.prepare_argument_types(
                data.method.signature.arguments.arguments
            )

            # Remove first argument, if method is not static
            # TODO: move into separated method
            if data.method.signature.arguments.arguments:
                arg_type = data.method.signature.arguments.arguments[0][
                    0].argument_type.names[0]
                arg_name = data.method.signature.arguments.arguments[0][0].name
                if data.class_name != 'constructor' and \
                        (
                                arg_type.lower() in white_list
                                or arg_type.lower() == data.class_name.lower()
                        ):
                    data.method.signature.arguments.arguments.pop(0)

                    if arg_name in data.method.docs.arguments:
                        del data.method.docs.arguments[arg_name]

    def prepare_resolve_multiple_signatures(self, data: FunctionOOP) -> \
            List[FunctionOOP]:
        if not data.method:
            return []

        out_list = [data.method]
        FilterDumpProcessFunctions.resolve_multiple_signatures(out_list, 0)
        if len(out_list) > 1:
            return list(
                map(
                    lambda list_data: FunctionOOP(
                        description=data.description,
                        class_name=data.class_name,
                        base_function_name=data.base_function_name,
                        method=list_data,
                        field=data.field,
                        is_static=data.is_static,
                    ),
                    out_list[1:]
                )
            )

        return []

    def prepare_class_name(self,
                           oop: FunctionOOP):
        """
        Prepares OOP class name
        """
        if '|' in oop.class_name:
            oop.class_name = re.match(self.CLASS_NAME_SELECTOR,
                                      oop.class_name).group(2)

        oop.class_name = oop.class_name.lower()
        oop.class_name = TypeConverter(oop.class_name).convert()

    def prepare_constructor(self,
                            oop: FunctionOOP,
                            function_base: FunctionData):
        """
        Prepares OOP constructor method
        """
        if oop.field is None and oop.is_static and oop.method is None:
            method = deepcopy(function_base)
            method.signature.name = 'constructor'

            oop.method = method
            oop.is_static = False

    def prepare_oop_definition(self,
                               side: ListType,
                               data_list_index: int,
                               data_list: List[FunctionOOP],
                               hashed_functions: Dict[
                                   str, CompoundFunctionData]) -> int:
        """
        Calls preparation method for the passed function.
        :return: New index in List[FunctionData]
        """
        data = data_list[data_list_index]
        function_base = hashed_functions[data.base_function_name][side][0]

        self.prepare_class_name(data)
        # Remove declarations without a class name
        if data.class_name == 'none':
            data_list.pop(data_list_index)
            return data_list_index

        increment = 1
        self.prepare_constructor(data, function_base)
        self.prepare_signature(data)
        to_insert = self.prepare_resolve_multiple_signatures(data)

        for oop in to_insert:
            data_list.insert(data_list_index, oop)
        increment += len(to_insert)

        return data_list_index + increment

    def apply(self):
        # TODO: Move into the context
        hashed_functions: Dict[str, CompoundFunctionData] = {
            **{
                function.client[0].name: function
                for function in self.context.functions
                if function.client
            },
            **{
                function.server[0].name: function
                for function in self.context.functions
                if function.server
            }
        }

        for oop in self.context.oops:
            for side, data_list in oop:
                data_list: List[FunctionOOP]

                index = 0
                while index < len(data_list):
                    index = self.prepare_oop_definition(
                        side=ListType[side.upper()],
                        data_list_index=index,
                        data_list=data_list,
                        hashed_functions=hashed_functions)

        print('\u001b[32mOOP Processing complete\u001b[0m')
