import pytest

from to_python.core.oop import OOPTokenizer
from to_python.core.tests.utils import compare_lists

TokenType = OOPTokenizer.TokenType


@pytest.mark.parametrize('code,expected', [
    (
            "{{OOP|The method name was incorrect (setPann'''n'''ingEnabled) before version '''1.5.8-9.20761.0'''.|[[sound]]:setPanningEnabled|panningEnabled|isSoundPanningEnabled}}}}",
            [
                OOPTokenizer.Token(type=TokenType.START, value='{{'),
                OOPTokenizer.Token(type=TokenType.UNUSED, value='OOP'),
                OOPTokenizer.Token(type=TokenType.DELIMITER, value='|'),
                OOPTokenizer.Token(
                    type=TokenType.NOTE,
                    value="The method name was incorrect (setPann'''n'''ingEnabled) before version '''1.5.8-9.20761.0'''."
                ),
                OOPTokenizer.Token(type=TokenType.DELIMITER, value='|'),
                OOPTokenizer.Token(type=TokenType.METHOD, value='[[sound]]:setPanningEnabled'),
                OOPTokenizer.Token(type=TokenType.DELIMITER, value='|'),
                OOPTokenizer.Token(type=TokenType.FIELD, value='panningEnabled'),
                OOPTokenizer.Token(type=TokenType.DELIMITER, value='|'),
                OOPTokenizer.Token(type=TokenType.COUNTERPART_METHOD, value='isSoundPanningEnabled'),
                OOPTokenizer.Token(type=TokenType.END, value='}}'),
                OOPTokenizer.Token(type=TokenType.END, value='}}')
            ]
    ),
    (
            "{{ OOP | As of MTA: SA {{Current Version|master}} the counterpart is not implemented yet. | [[browser]]:setRenderingPaused | renderingPaused | isBrowserRenderingPaused }}",
            [
                OOPTokenizer.Token(type=TokenType.START, value='{{'),
                OOPTokenizer.Token(type=TokenType.UNUSED, value='OOP'),
                OOPTokenizer.Token(type=TokenType.DELIMITER, value='|'),
                OOPTokenizer.Token(
                    type=TokenType.NOTE,
                    value='As of MTA: SA {{Current Version|master}} the counterpart is not implemented yet.'
                ),
                OOPTokenizer.Token(type=TokenType.DELIMITER, value='|'),
                OOPTokenizer.Token(type=TokenType.METHOD, value='[[browser]]:setRenderingPaused'),
                OOPTokenizer.Token(type=TokenType.DELIMITER, value='|'),
                OOPTokenizer.Token(type=TokenType.FIELD, value='renderingPaused'),
                OOPTokenizer.Token(type=TokenType.DELIMITER, value='|'),
                OOPTokenizer.Token(type=TokenType.COUNTERPART_METHOD, value='isBrowserRenderingPaused'),
                OOPTokenizer.Token(type=TokenType.END, value='}}')
            ]
    ),
    (
            "{{ OOP | | [[blip]]:setVisibleDistance | visibleDistance | getBlipVisibleDistance | }}",
            [
                OOPTokenizer.Token(type=TokenType.START, value='{{'),
                OOPTokenizer.Token(type=TokenType.UNUSED, value='OOP'),
                OOPTokenizer.Token(type=TokenType.DELIMITER, value='|'),
                OOPTokenizer.Token(type=TokenType.DELIMITER, value='|'),
                OOPTokenizer.Token(type=TokenType.METHOD, value='[[blip]]:setVisibleDistance'),
                OOPTokenizer.Token(type=TokenType.DELIMITER, value='|'),
                OOPTokenizer.Token(type=TokenType.FIELD, value='visibleDistance'),
                OOPTokenizer.Token(type=TokenType.DELIMITER, value='|'),
                OOPTokenizer.Token(type=TokenType.COUNTERPART_METHOD, value='getBlipVisibleDistance'),
                OOPTokenizer.Token(type=TokenType.DELIMITER, value='|'),
                OOPTokenizer.Token(type=TokenType.END, value='}}')
            ]
    ),
])
def test_oop_tokenizer(code, expected):
    compare_lists(OOPTokenizer(code).tokenize(), expected)
