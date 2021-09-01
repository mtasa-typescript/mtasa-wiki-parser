# See https://github.com/mtasa-typescript/mtasa-wiki-parser/issues/32
from to_python.core.types import FunctionData, FunctionDoc, FunctionSignature, FunctionReturnTypes, \
    FunctionArgumentValues, FunctionType, FunctionArgument

dx_create_texture_function: FunctionData = FunctionData(
    docs=FunctionDoc(
        description='This function creates a texture element that can be used in the dxDraw functions',
        arguments={},
        result='Returns a texture if successful, false if invalid arguments were passed to the function.'
    ),
    signature=FunctionSignature(
        name='dxCreateTexture',
        return_types=FunctionReturnTypes(
            return_types=[
                FunctionType(
                    is_optional=False,
                    names=['Element']
                )
            ],
            variable_length=False,
        ),
        arguments=FunctionArgumentValues(
            arguments=[
                [FunctionArgument(
                    name='width',
                    argument_type=FunctionType(
                        is_optional=False,
                        names=['number']
                    ),
                    default_value=None,
                )],
                [FunctionArgument(
                    name='height',
                    argument_type=FunctionType(
                        is_optional=False,
                        names=['number']
                    ),
                    default_value=None,
                )],
                [FunctionArgument(
                    name='textureFormat',
                    argument_type=FunctionType(
                        is_optional=True,
                        names=['string']
                    ),
                    default_value='"argb',
                )],
                [FunctionArgument(
                    name='textureEdge',
                    argument_type=FunctionType(
                        is_optional=True,
                        names=['string']
                    ),
                    default_value='"wrap',
                )],
                [FunctionArgument(
                    name='textureType',
                    argument_type=FunctionType(
                        is_optional=True,
                        names=['string']
                    ),
                    default_value='"2d',
                )],
                [FunctionArgument(
                    name='depth',
                    argument_type=FunctionType(
                        is_optional=True,
                        names=['number']
                    ),
                    default_value='1',
                )],
            ],
            variable_length=False,
        ),
    )
)
