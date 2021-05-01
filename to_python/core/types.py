from dataclasses import dataclass
from typing import List, Dict, Optional

from crawler.core.types import FunctionUrl


@dataclass
class FunctionType:
    """
    Type description
    """
    names: List[str]  # Type unions
    is_optional: bool

    def __repr__(self):
        return f'''FunctionType(
                        names={repr(self.names)},
                        is_optional={self.is_optional},
                    )'''


@dataclass
class FunctionArgument:
    """
    Argument data
    """
    name: str
    argument_type: FunctionType
    default_value: Optional[str]

    def __repr__(self):
        return f'''FunctionArgument(
                    name='{self.name}',
                    argument_type={repr(self.argument_type)},
                    default_value={repr(self.default_value)},
                )'''


@dataclass
class FunctionArgumentValues:
    """
    Function arguments
    """
    arguments: List[List[FunctionArgument]]
    variable_length: bool

    def __repr__(self):
        arguments_list = []
        for v in self.arguments:
            result_list = [repr(argument) for argument in v]
            arguments_list.append(',\n                '.join(result_list))

        arguments = ',\n            '.join([f'[\n                {v}\n            ]'
                                            for v in arguments_list])
        return f'''FunctionArgumentValues(
        arguments=[
            {arguments}
        ],
        variable_length={self.variable_length},
    )'''


@dataclass
class FunctionReturnTypes:
    """
    Function return types
    """
    return_types: List[FunctionType]
    variable_length: bool

    def __repr__(self):
        return_types = ',\n            '.join([repr(v) for v in self.return_types])
        return f'''FunctionReturnTypes(
        return_types=[
            {return_types}
        ],
        variable_length={self.variable_length},
    )'''


@dataclass
class FunctionSignature:
    """
    Function information (default style)
    """
    name: str
    return_types: FunctionReturnTypes
    arguments: FunctionArgumentValues

    def __repr__(self):
        return f'''FunctionSignature(
    name='{self.name}',
    return_types={repr(self.return_types)},
    arguments={repr(self.arguments)},
)'''


@dataclass
class FunctionDoc:
    """
    Docs for function
    """
    description: str
    arguments: Dict[str, str]
    result: str

    def __repr__(self):
        return f'''FunctionDoc(
    description='{self.description}',
    arguments='{repr(self.arguments)}',
    result='{self.result}',
)'''


@dataclass
class FunctionOOP:
    """
    Function OOP information
    """
    description: Optional[str]
    class_name: str
    method_name: Optional[str]
    field: Optional[str]
    is_static: bool

    def __repr__(self):
        return f'''FunctionOOP(
        description='{self.description}',
        class_name='{self.class_name}',
        method_name='{self.method_name}',
        field='{self.field}',
        is_static='{self.is_static}',
    )'''


@dataclass
class FunctionData:
    """
    All function data from wiki
    """
    signature: FunctionSignature
    docs: FunctionDoc
    oop: Optional[FunctionOOP]
    name: str

    def __repr__(self):
        return f'''FunctionData(
    signature='{repr(self.signature)}',
    docs='{repr(self.docs)}',
    oop='{repr(self.oop)}',
    name='{self.name}',
)'''


@dataclass
class CompoundFunctionData:
    """
    Data about client-side and server-side function
    """
    server: Optional[FunctionData] = None
    client: Optional[FunctionData] = None

    def __repr__(self):
        return f'''FunctionData(
    server='{repr(self.server)}',
    client='{repr(self.client)}',
)'''
