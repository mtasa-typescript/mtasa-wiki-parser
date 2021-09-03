from copy import deepcopy
from typing import List

from to_python.core.types import CompoundFunctionData
from to_typescript.filters.processing_post import get_functions_from_list_by_name, ListType
from to_typescript.mixins.data.dx_create_texture import dx_create_texture_function


def mixin_function(function_list: List[CompoundFunctionData]):
    data = get_functions_from_list_by_name(function_list, ListType.CLIENT, 'dxCreateTexture')[-1][0]
    function_list.insert(
        function_list.index(data) + 1,
        CompoundFunctionData(
            client=[
                deepcopy(dx_create_texture_function)
            ],
            server=[]
        )
    )
