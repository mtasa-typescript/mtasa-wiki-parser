import pytest

from src.fetch.fetch_function import get_function_data, parse_get_function_signature, parse_get_function_arguments_docs
from src.fetch.function import FunctionUrl, ListType


@pytest.fixture
def gui_get_screen_size_url() -> FunctionUrl:
    return FunctionUrl(url='/wiki/GuiGetScreenSize',
                       name='guiGetScreenSize',
                       category='GUI functions',
                       function_type=ListType.CLIENT, )


@pytest.fixture
def dx_draw_text_url() -> FunctionUrl:
    return FunctionUrl(url='/wiki/DxDrawText',
                       name='dxDrawText',
                       category='Drawing functions',
                       function_type=ListType.CLIENT, )


@pytest.fixture
def get_element_by_id_url() -> FunctionUrl:
    return FunctionUrl(url='/wiki/GetElementByID',
                       name='getElementByID',
                       category='Element functions',
                       function_type=ListType.CLIENT, )


def test_get_function_gui_get_screen_size(gui_get_screen_size_url):
    result = get_function_data(gui_get_screen_size_url)
    assert result is not None


def test_parse_get_function_signature_correct_empty_function():
    code = f'''float float guiGetScreenSize()'''
    function_type = parse_get_function_signature(code)

    assert len(function_type.arguments) == 0

    assert function_type.name == 'guiGetScreenSize'
    assert function_type.return_types == ['float', 'float', ]


def test_parse_get_function_signature_correct_element_function():
    code = f'''element getElementByID ( string id [, int index = 0 ] ) '''
    function_type = parse_get_function_signature(code)

    assert function_type.arguments[0].name == 'id'
    assert function_type.arguments[0].argument_type == 'string'
    assert function_type.arguments[0].default_value is None
    assert function_type.arguments[0].optional is False

    assert function_type.arguments[1].name == 'index'
    assert function_type.arguments[1].argument_type == 'int'
    assert function_type.arguments[1].default_value == '0'
    assert function_type.arguments[1].optional is True

    assert function_type.name == 'getElementByID'
    assert function_type.return_types == ['element', ]


def test_parse_get_function_arguments_docs():
    code = f"""
==Syntax== 
<syntaxhighlight lang="lua">bool setSoundVolume ( element theSound/thePlayer, float volume )</syntaxhighlight> 
{{OOP||[[sound]]:setVolume|volume|getSoundVolume}}
===Required Arguments=== 
*'''theSound:''' The [[sound]] [[element]] which volume you want to modify or a [[player]] element which voice volume you want to modify.
*'''volume:''' A [[float]]ing point number representing the desired volume level. Range is from '''0.0''' to '''1.0'''. This can go above '''1.0''' for amplification.

===Returns===
Returns ''true'' if the [[sound]] [[element]] volume was successfully changed, ''false'' otherwise.
"""

    result = parse_get_function_arguments_docs(code)
    assert result == {
        'theSound': 'The sound element which volume you want to modify or a player '
                    'element which voice volume you want to modify.',
        'volume': 'A floating point number representing the desired volume level. '
                  'Range is from 0.0 to 1.0. This can go above 1.0 for amplification.'
    }


def test_parse_get_function_arguments_docs_with_optional():
    code = f"""
==Syntax== 
<syntaxhighlight lang="lua">table getSoundFFTData ( element sound, int iSamples [, int iBands = 0 ] )</syntaxhighlight> 
{{OOP||[[sound]]:getFFTData}}
===Required Arguments=== 
*'''sound:''' a sound element that is created using [[playSound]] or [[playSound3D]]. Streams are also supported
*'''iSamples:''' allowed samples are 256, 512, 1024, 2048, 4096, 8192 and 16384.

===Optional Arguments===
*'''iBands:''' post processing option allows you to split the samples into the desired amount of bands or bars so if you only need 5 bars this saves a lot of cpu power compared to trying to do it in Lua.

===Returns===
Returns a table of '''iSamples'''/2 (or '''iBands''' if '''iBands''' is used) ''floats'' representing the current audio frame.
Returns ''false'' if the sound is not playing yet or hasn't buffered in the
case of streams.
"""

    result = parse_get_function_arguments_docs(code)
    assert result
