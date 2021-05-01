from typing import Optional

from to_python.core.types import FunctionType


class TypeConverter:
    """
    Converts MTASA Wiki types into TypeScript types
    """

    def __init__(self, arg_type: str):
        self.arg_type = arg_type

    def convert(self) -> str:
        return self.arg_type and 'any'

    @staticmethod
    def is_varargs_type(type_name: Optional[FunctionType]) -> bool:
        if type_name is None:
            return True

        if 'var' in [name.lower().strip() for name in type_name.names]:
            return True

        return False