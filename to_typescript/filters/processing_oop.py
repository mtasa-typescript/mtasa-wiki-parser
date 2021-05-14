import re
from typing import List

from to_python.core.types import FunctionData, FunctionOOP
from to_typescript.core.filter import FilterAbstract
from to_typescript.core.transform.extra_rules import TypeConverter


class FilterDumpProcessOOP(FilterAbstract):
    """
    Post processing for dumps (OOP).
    Argument types changes, custom types, names, argument names, return types
    or additional information can be provided here
    """

    CLASS_NAME_SELECTOR = re.compile(r'^([^|]*\|(.+))$')

    def prepare_class_name(self,
                           oop: FunctionOOP):
        """
        Prepares OOP class name
        """
        if '|' in oop.class_name:
            oop.class_name = re.match(self.CLASS_NAME_SELECTOR, oop.class_name).group(2)

        oop.class_name = oop.class_name.lower()
        oop.class_name = TypeConverter(oop.class_name).convert()

    def prepare_constructor(self,
                            oop: FunctionOOP):
        """
        Prepares OOP constructor method
        """
        if oop.field is None and oop.is_static and oop.method_name is None:
            oop.method_name = 'constructor'
            oop.is_static = False

    def prepare_oop_definition(self,
                               data_list_index: int,
                               data_list: List[FunctionData]) -> int:
        """
        Calls preparation method for the passed function.
        :return: New index in List[FunctionData]
        """
        increment = 1

        data = data_list[data_list_index]
        if data.oop is None:
            return data_list_index + increment

        self.prepare_class_name(data.oop)
        self.prepare_constructor(data.oop)

        # Remove declarations without a class name
        if data.oop.class_name == 'none':
            data.oop = None

        return data_list_index + increment

    def apply(self):
        for function in self.context.functions:
            for side, data_list in function:

                index = 0
                while index < len(data_list):
                    index = self.prepare_oop_definition(data_list_index=index,
                                                        data_list=data_list)
