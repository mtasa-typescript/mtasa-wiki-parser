from copy import deepcopy
from typing import List

from to_python.core.types import CompoundFunctionData
from to_typescript.mixins.data.dx_create_texture import dx_create_texture_function


def mixin_function(function_list: List[CompoundFunctionData]):
    function_list.append(
        CompoundFunctionData(
            client=[
                deepcopy(dx_create_texture_function)
            ],
            server=[]
        )
    )
