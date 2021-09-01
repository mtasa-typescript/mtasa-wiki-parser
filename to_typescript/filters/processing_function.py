from copy import copy, deepcopy
from typing import List

from to_python.core.types import FunctionData, FunctionDoc, FunctionArgument, FunctionType
from to_typescript.core.filter import FilterAbstract
from to_typescript.core.transform.extra_rules import TypeConverter


class FilterDumpProcessFunctions(FilterAbstract):
    """
    Post processing for dumps.
    Argument types changes, custom types, names, argument names, return types
    or additional information can be provided here
    """

    def remove_utf8(self):
        """
        Removed UTF8 category. It should be processed manually
        """
        # TODO: process UTF8 category
        index = 0
        while index < len(self.context.functions):
            f = self.context.functions[index]
            url = self.context.urls[(f.server or f.client)[0].name]

            # Something like blacklist workaround
            if url.category.lower() in {
                'utf8 library',
            }:
                self.context.functions.pop(index)
                continue

            index += 1

    @staticmethod
    def prepare_argument_names(arguments: List[List[FunctionArgument]]):
        """
        Cleans the argument names from forbidden characters  for a single function
        """
        for argument_list in arguments:
            for argument in argument_list:
                name = argument.name
                if name:

                    if name == 'var':
                        argument.name = 'variable'

                    argument.name = argument.name.replace('/', '_')
                    argument.name = argument.name.replace('-', '_')

    @staticmethod
    def prepare_argument_types(arguments: List[List[FunctionArgument]]):
        """
        Convert types for a single function
        """

        for argument_list in arguments:
            for argument in argument_list:
                types = argument.argument_type
                if types:
                    types.names = [TypeConverter(name).convert() for name in types.names]

    @staticmethod
    def prepare_return_types(return_types: List[FunctionType]):
        """
        Convert types for a single function
        """
        # Argument types

        # Return types
        for return_type in return_types:
            return_type.names = [TypeConverter(name).convert() for name in return_type.names]

    @staticmethod
    def resolve_multiple_signatures(data_list: List[FunctionData],
                                    index_in_list: int) -> bool:
        """
        Example: export function fun(a?: int, b: int): int;
        Will be splitted into
        export function fun(a: int, b: int): int; // and
        export function fun(b: int): int;
        :return: Should index be saved (not incremented)
        """
        index_should_be_increased = True

        data = data_list[index_in_list]
        signature = data.signature

        first_optional_index = -1
        for index, argument_list in enumerate(signature.arguments.arguments):
            is_optional = len([argument
                               for argument in argument_list
                               if argument.argument_type and argument.argument_type.is_optional]) != 0

            if len([argument
                    for argument in argument_list
                    if not argument.argument_type]) != 0:
                is_optional = True

            if is_optional:
                if first_optional_index == -1:
                    first_optional_index = index

                continue

            if not is_optional:
                if first_optional_index == -1:
                    continue

                # There were optional arguments. And the current is a required argument
                index_should_be_increased = False
                new_signature = deepcopy(signature)

                # Remove (index - first_optional_index - 1) arguments from the new signature
                for _ in range(first_optional_index, index):
                    new_signature.arguments.arguments.pop(first_optional_index)

                # Make arguments required in the origin signature
                for i in range(first_optional_index, index):
                    for arg in signature.arguments.arguments[i]:
                        if not arg.argument_type:
                            continue

                        arg.argument_type.is_optional = False

                # Save the new signature
                data_list.append(FunctionData(signature=new_signature,
                                              docs=FunctionDoc(description='',
                                                               arguments=dict(),
                                                               result='', ), ), )
                first_optional_index = -1

        return index_should_be_increased

    def prepare_function(self,
                         data_list_index: int,
                         data_list: List[FunctionData]) -> int:
        """
        Calls preparation method for the passed function.
        :return: New index in List[FunctionData]
        """
        increment = 1

        data = data_list[data_list_index]
        self.prepare_argument_names(data.signature.arguments.arguments)
        self.prepare_argument_types(data.signature.arguments.arguments)
        self.prepare_return_types(data.signature.return_types.return_types)

        increment = +self.resolve_multiple_signatures(data_list=data_list,
                                                      index_in_list=data_list_index)

        return data_list_index + increment

    def apply(self):
        self.remove_utf8()
        print('\u001b[33mWarning:\u001b[0m UTF8 category has been removed from processing. '
              'See https://github.com/mtasa-typescript/mtasa-wiki-parser/issues/31\u001b[0m')

        for function in self.context.functions:
            for side, data_list in function:

                index = 0
                while index < len(data_list):
                    index = self.prepare_function(data_list_index=index,
                                                  data_list=data_list)

        print('\u001b[32mFunction processing complete\u001b[0m')

