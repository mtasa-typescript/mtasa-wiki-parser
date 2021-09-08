from typing import List

from to_python.core.types import CompoundOOPData, FunctionOOP, FunctionType, \
    FunctionArgument
from to_typescript.filters.processing_post import get_oops_from_list_by_name, \
    ListType


def each_oop_data_from_list_by_name(f_list: List[CompoundOOPData],
                                    function_type: ListType,
                                    function_name: str):
    for oop_data, _ in get_oops_from_list_by_name(f_list, function_type,
                                                  function_name):
        for side, inner_list in oop_data:
            for data in inner_list:
                data: FunctionOOP
                yield data


def mixin_oop(oop_list: List[CompoundOOPData]):
    for data in each_oop_data_from_list_by_name(oop_list, ListType.SHARED,
                                                'getColShapeSize'):
        data.method.signature.return_types.return_types = [
            FunctionType(
                is_optional=False,
                names=[
                    'number',
                    'Vector2',
                    'Vector3',
                ]
            )
        ]

    for data in each_oop_data_from_list_by_name(oop_list, ListType.SHARED,
                                                'setColShapeSize'):
        data.method.signature.arguments.arguments = [
            [
                FunctionArgument(
                    default_value=None,
                    argument_type=FunctionType(
                        is_optional=False,
                        names=[
                            'number',
                            'Vector2',
                            'Vector3',
                        ]
                    ),
                    name='vectorized'
                )
            ]
        ]

    for data in each_oop_data_from_list_by_name(oop_list, ListType.SHARED,
                                                'getElementBoundingBox'):
        data.method.signature.return_types.return_types = [
            FunctionType(
                is_optional=False,
                names=[
                    'Vector3',
                ]
            ),
            FunctionType(
                is_optional=False,
                names=[
                    'Vector3',
                ]
            )
        ]

    for data in each_oop_data_from_list_by_name(oop_list, ListType.SHARED,
                                                'setElementBoundingBox'):
        data.method.signature.arguments.arguments = [
            [
                FunctionArgument(
                    default_value=None,
                    argument_type=FunctionType(
                        is_optional=False,
                        names=[
                            'Vector3',
                        ]
                    ),
                    name='vectorized'
                )
            ],
        ]
