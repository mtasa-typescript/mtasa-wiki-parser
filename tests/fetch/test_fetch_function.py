import pytest

from src.fetch.fetch_function import get_function_data, parse_get_function_signature, parse_get_function_arguments_docs, \
    parse_get_function_returns_doc, parse, parse_get_function_type, ParseFunctionType
from src.fetch.function import FunctionUrl, ListType, CompoundFunctionData, FunctionDoc, FunctionArgument, FunctionType, \
    FunctionData, FunctionOOP


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
    assert result == {
        'sound': 'a sound element that is created using playSound or playSound3D. Streams are also supported',
        'iSamples': 'allowed samples are 256, 512, 1024, 2048, 4096, 8192 and 16384.',
        'iBands': 'post processing option allows you to split the samples into the '
                  'desired amount of bands or bars so if you only need 5 bars'
                  ' this saves a lot of cpu power compared to trying to do it in Lua.'
    }


def test_parse_get_function_arguments_docs_empty():
    code = ''
    result = parse_get_function_arguments_docs(code)
    assert result == {}


def test_parse_get_function_returns_doc_correct():
    code = f"""==Syntax== 
<syntaxhighlight lang="lua">bool setBlipOrdering ( blip theBlip, int ordering )</syntaxhighlight>
{{OOP||[[blip]]:setOrdering|ordering|getBlipOrdering|}}
===Required Arguments===
*'''theBlip:''' the blip whose Z ordering to change.
*'''ordering:''' the new Z ordering value. Blips with higher values will appear on top of blips with lower values. Possible range: -32767 to 32767. Default: 0.

===Returns===
Returns ''true'' if the blip ordering was changed successfully, ''false'' otherwise.

==Example==
This example will create a blip and make your blip on top of all other blip's.
<section class="server" name="Server" show="true">
<syntaxhighlight lang="lua">"""

    result = parse_get_function_returns_doc(code)
    assert result == """Returns ''true'' if the blip ordering was changed successfully, ''false'' otherwise."""


def test_parse_get_function_returns_doc_empty():
    code = ''
    result = parse_get_function_returns_doc(code)
    assert result == ''


def test_parse_get_function_type_with_comment():
    code = '''__NOTOC__ 
{{Server function}}<!-- Change this to "Client function" or "Server function" appropriately-->
<!-- Describe in plain english what this function does. Don't go into details, just give an overview -->
This function returns a table over all the ACL's that exist in a given ACL group.'''

    result = parse_get_function_type(code)
    assert result == ParseFunctionType.SERVER


def test_parse_get_function_signature_with_commas():
    code = '''int, int, int getTeamColor ( team theTeam )'''

    result = parse_get_function_signature(code)
    assert result == FunctionType(name='getTeamColor',
                                  return_types=['int', 'int', 'int'],
                                  arguments=[
                                      FunctionArgument(name='theTeam',
                                                       argument_type='team',
                                                       default_value=None,
                                                       optional=False)
                                  ])


def test_parse_get_function_signature_with_dot_in_function_name():
    code = '''int, int utf8.find ( string input, string pattern [, int startpos = 1, boolean plain = false ] )'''

    result = parse_get_function_signature(code)
    assert result == FunctionType(name='utf8.find',
                                  return_types=['int', 'int'],
                                  arguments=[
                                      FunctionArgument(name='input',
                                                       argument_type='string',
                                                       default_value=None,
                                                       optional=False),
                                      FunctionArgument(name='pattern',
                                                       argument_type='string',
                                                       default_value=None,
                                                       optional=False),
                                      FunctionArgument(name='startpos',
                                                       argument_type='int',
                                                       default_value='1',
                                                       optional=True),
                                      FunctionArgument(name='plain',
                                                       argument_type='boolean',
                                                       default_value='false',
                                                       optional=True)
                                  ])
