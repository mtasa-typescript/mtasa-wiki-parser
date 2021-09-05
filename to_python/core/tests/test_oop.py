import pytest

from to_python.core.oop import OOPTokenizer, OOPParser
from to_python.core.tests.utils import compare_lists
from to_python.core.types import FunctionType, FunctionReturnTypes, \
    FunctionData, FunctionSignature, \
    FunctionArgumentValues, FunctionArgument, FunctionDoc, FunctionOOPField
from to_python.filters.data_list.oop import FilterParseFunctionOOP

TokenType = OOPTokenizer.TokenType


@pytest.mark.parametrize('code,expected', [
    (
            "{{OOP|The method name was incorrect (setPann'''n'''ingEnabled) "
            "before version '''1.5.8-9.20761.0'''.|[[sound]]:setPanningEnabled"
            "|panningEnabled|isSoundPanningEnabled}}}}",
            [
                OOPTokenizer.Token(type=TokenType.START, value='{{'),
                OOPTokenizer.Token(type=TokenType.UNUSED, value='OOP'),
                OOPTokenizer.Token(type=TokenType.DELIMITER, value='|'),
                OOPTokenizer.Token(
                    type=TokenType.NOTE,
                    value="The method name was incorrect "
                          "(setPann'''n'''ingEnabled) before version "
                          "'''1.5.8-9.20761.0'''."
                ),
                OOPTokenizer.Token(type=TokenType.DELIMITER, value='|'),
                OOPTokenizer.Token(type=TokenType.METHOD,
                                   value='[[sound]]:setPanningEnabled'),
                OOPTokenizer.Token(type=TokenType.DELIMITER, value='|'),
                OOPTokenizer.Token(type=TokenType.FIELD,
                                   value='panningEnabled'),
                OOPTokenizer.Token(type=TokenType.DELIMITER, value='|'),
                OOPTokenizer.Token(type=TokenType.COUNTERPART_METHOD,
                                   value='isSoundPanningEnabled'),
                OOPTokenizer.Token(type=TokenType.END, value='}}'),
                OOPTokenizer.Token(type=TokenType.END, value='}}')
            ]
    ),
    (
            "{{ OOP | As of MTA: SA {{Current Version|master}} the "
            "counterpart is not implemented yet. | [[browser]]:"
            "setRenderingPaused | renderingPaused | "
            "isBrowserRenderingPaused }}",
            [
                OOPTokenizer.Token(type=TokenType.START, value='{{'),
                OOPTokenizer.Token(type=TokenType.UNUSED, value='OOP'),
                OOPTokenizer.Token(type=TokenType.DELIMITER, value='|'),
                OOPTokenizer.Token(
                    type=TokenType.NOTE,
                    value='As of MTA: SA {{Current Version|master}} '
                          'the counterpart is not implemented yet.'
                ),
                OOPTokenizer.Token(type=TokenType.DELIMITER, value='|'),
                OOPTokenizer.Token(type=TokenType.METHOD,
                                   value='[[browser]]:setRenderingPaused'),
                OOPTokenizer.Token(type=TokenType.DELIMITER, value='|'),
                OOPTokenizer.Token(type=TokenType.FIELD,
                                   value='renderingPaused'),
                OOPTokenizer.Token(type=TokenType.DELIMITER, value='|'),
                OOPTokenizer.Token(type=TokenType.COUNTERPART_METHOD,
                                   value='isBrowserRenderingPaused'),
                OOPTokenizer.Token(type=TokenType.END, value='}}')
            ]
    ),
    (
            "{{ OOP | | [[blip]]:setVisibleDistance "
            "| visibleDistance | getBlipVisibleDistance | }}",
            [
                OOPTokenizer.Token(type=TokenType.START, value='{{'),
                OOPTokenizer.Token(type=TokenType.UNUSED, value='OOP'),
                OOPTokenizer.Token(type=TokenType.DELIMITER, value='|'),
                OOPTokenizer.Token(type=TokenType.DELIMITER, value='|'),
                OOPTokenizer.Token(type=TokenType.METHOD,
                                   value='[[blip]]:setVisibleDistance'),
                OOPTokenizer.Token(type=TokenType.DELIMITER, value='|'),
                OOPTokenizer.Token(type=TokenType.FIELD,
                                   value='visibleDistance'),
                OOPTokenizer.Token(type=TokenType.DELIMITER, value='|'),
                OOPTokenizer.Token(type=TokenType.COUNTERPART_METHOD,
                                   value='getBlipVisibleDistance'),
                OOPTokenizer.Token(type=TokenType.DELIMITER, value='|'),
                OOPTokenizer.Token(type=TokenType.END, value='}}')
            ]
    ),
])
def test_oop_tokenizer(code, expected):
    compare_lists(OOPTokenizer(code).tokenize(), expected)


def test_oop_parse_metadata():
    oop_code = '{{OOP||[[light]]:getColor|color|setLightColor}}'
    result = OOPParser(OOPTokenizer(oop_code).tokenize()).parse()
    assert result == OOPParser.OutputData(
        misc_description=None,
        field_name='color',
        method_data=OOPParser.MethodData(
            class_name='light',
            is_static=False,
            method_name='getColor',
        )
    )


def test_oop_parse_method_and_field():
    oop_code = '{{OOP||[[light]]:getColor|color|setLightColor}}'

    function_data = FunctionData(
        url='getLightColor',
        signature=FunctionSignature(
            name='getLightColor',
            return_types=FunctionReturnTypes(
                return_types=[
                    FunctionType(
                        names=['int'],
                        is_optional=False,
                    ),
                    FunctionType(
                        names=['int'],
                        is_optional=False,
                    ),
                    FunctionType(
                        names=['int'],
                        is_optional=False,
                    )
                ],
                variable_length=False,
            ),
            arguments=FunctionArgumentValues(
                arguments=[
                    [
                        FunctionArgument(
                            name='theLight',
                            argument_type=FunctionType(
                                names=['light'],
                                is_optional=False,
                            ),
                            default_value=None,
                        )
                    ]
                ],
                variable_length=False,
            ),
            generic_types=[

            ],
        ),
        docs=FunctionDoc(
            description='',
            arguments={},
            result='',
        ),
    )
    oop_metadata = OOPParser(OOPTokenizer(oop_code).tokenize()).parse()

    method = FilterParseFunctionOOP.prepare_oop_method(
        oop_metadata,
        function_data
    )
    field = FilterParseFunctionOOP.prepare_oop_field(
        oop_metadata,
        function_data.signature.return_types
    )

    assert method == FunctionData(
        url='getLightColor',
        signature=FunctionSignature(
            name='getColor',
            return_types=FunctionReturnTypes(
                return_types=[
                    FunctionType(
                        names=['int'],
                        is_optional=False,
                    ),
                    FunctionType(
                        names=['int'],
                        is_optional=False,
                    ),
                    FunctionType(
                        names=['int'],
                        is_optional=False,
                    )
                ],
                variable_length=False,
            ),
            arguments=FunctionArgumentValues(
                arguments=[
                    [
                        FunctionArgument(
                            name='theLight',
                            argument_type=FunctionType(
                                names=['light'],
                                is_optional=False,
                            ),
                            default_value=None,
                        )
                    ]
                ],
                variable_length=False,
            ),
            generic_types=[

            ],
        ),
        docs=FunctionDoc(
            description='',
            arguments={

            },
            result='',
        )
    )

    assert field == FunctionOOPField(
        name='color',
        types=[
            FunctionType(
                names=['int'],
                is_optional=False,
            ),
            FunctionType(
                names=['int'],
                is_optional=False,
            ),
            FunctionType(
                names=['int'],
                is_optional=False,
            )
        ],
    )
