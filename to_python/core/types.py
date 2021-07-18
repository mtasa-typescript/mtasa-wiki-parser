from copy import copy
from dataclasses import dataclass, field
from typing import List, Dict, Optional

from crawler.core.types import ListType


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

    def __copy__(self):
        return FunctionType(names=copy(self.names),
                            is_optional=self.is_optional)


@dataclass
class FunctionArgument:
    """
    Argument data
    """
    name: str
    argument_type: Optional[FunctionType]
    default_value: Optional[str]

    def __repr__(self):
        return f'''FunctionArgument(
                                name='{self.name}',
                                argument_type={repr(self.argument_type)},
                                default_value={repr(self.default_value)},
                            )'''

    def __copy__(self):
        return FunctionArgument(name=self.name,
                                argument_type=copy(self.argument_type),
                                default_value=self.default_value)


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

        arguments = f',\n{" " * 24}'.join([f'[\n{" " * 28}{v}\n{" " * 24}]'
                                           for v in arguments_list])
        return f'''FunctionArgumentValues(
                    arguments=[
                        {arguments}
                    ],
                    variable_length={self.variable_length},
                )'''

    def __copy__(self):
        return FunctionArgumentValues(arguments=copy(self.arguments),
                                      variable_length=self.variable_length)


@dataclass
class FunctionReturnTypes:
    """
    Function return types
    """
    return_types: List[FunctionType]
    variable_length: bool

    def __repr__(self):
        return_types = f',\n{" " * 20}'.join([repr(v) for v in self.return_types])
        return f'''FunctionReturnTypes(
                    return_types=[
                        {return_types}
                    ],
                    variable_length={self.variable_length},
                )'''

    def __copy__(self):
        return FunctionReturnTypes(return_types=copy(self.return_types),
                                   variable_length=self.variable_length)


@dataclass
class FunctionGeneric:
    """
    Generic type information
    """
    name: str
    extends: Optional[str]
    default_value: Optional[str]

    def __repr__(self):
        return f'''FunctionGeneric(
                        name='{self.name}',
                        extends{self.extends}',
                        default_value={repr(self.default_value)},
                    )'''


@dataclass
class FunctionSignature:
    """
    Function information (default style)
    """
    name: str
    return_types: FunctionReturnTypes
    arguments: FunctionArgumentValues
    generic_types: List[FunctionGeneric] = field(default_factory=list)

    def __repr__(self):
        generics = f',\n{" " * 20}'.join([repr(v) for v in self.generic_types])
        return f'''FunctionSignature(
                name='{self.name}',
                return_types={repr(self.return_types)},
                arguments={repr(self.arguments)},
                generic_types=[
                    {generics}
                ],
            )'''

    def __copy__(self):
        return FunctionSignature(name=self.name,
                                 return_types=copy(self.return_types),
                                 arguments=copy(self.arguments))


@dataclass
class FunctionDoc:
    """
    Docs for function
    """
    description: str
    arguments: Dict[str, str]
    result: str

    def __repr__(self):
        dict_text = (f'{{\n{" " * 20}'
                     + f',\n{" " * 20}'.join(f'"{k}": """{self.arguments[k]} """' for k in self.arguments)
                     + f'\n{" " * 16}}}')

        return f'''FunctionDoc(
                description="""{self.description} """,
                arguments={dict_text},
                result="""{self.result} """,
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
        p_description = f'"""{self.description}"""' if self.description else 'None'
        p_method_name = f'"""{self.method_name}"""' if self.method_name else 'None'
        p_field = f'"""{self.field}"""' if self.field else 'None'

        return f'''FunctionOOP(
                description={p_description},
                class_name='{self.class_name}',
                method_name={p_method_name},
                field={p_field},
                is_static={self.is_static},
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
            signature={repr(self.signature)},
            docs={repr(self.docs)},
            oop={repr(self.oop)},
            name='{self.name}',
        )'''


@dataclass
class CompoundFunctionData:
    """
    Data about client-side and server-side function
    """
    server: List[FunctionData] = field(default_factory=list)
    client: List[FunctionData] = field(default_factory=list)

    def __repr__(self):
        server = f',\n{" " * 12}'.join([repr(v) for v in self.server])
        client = f',\n{" " * 12}'.join([repr(v) for v in self.client])
        return f'''CompoundFunctionData(
        server=[
            {server}
        ],
        client=[
            {client}
        ],
    )'''

    def __iter__(self):
        if self.server:
            yield 'server', self.server

        if self.client:
            yield 'client', self.client

    def __getitem__(self, item: ListType):
        """
        Allows [] operation
        """
        if item == ListType.CLIENT:
            return self.client

        if item == ListType.SERVER:
            return self.server

        return None


@dataclass
class EventData:
    """
    Data about the event
    """
    arguments_values: List[FunctionArgumentValues]
    docs: FunctionDoc
    name: str

    def __repr__(self):
        values = f',\n{" " * 20}'.join([repr(v) for v in self.arguments_values])
        return f'''FunctionData(
            name='{self.name}',
            docs={repr(self.docs)},
            values=[
                {values}
            ],
        )'''


@dataclass
class CompoundEventData:
    """
    Data about event
    """
    events: List[EventData] = field(default_factory=list)

    def __repr__(self):
        events = f',\n{" " * 12}'.join([repr(v) for v in self.events])
        return f'''CompoundEventData(
        events=[
            {events}
        ],
    )'''
