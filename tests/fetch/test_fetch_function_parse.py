import pytest

from src.fetch.fetch_function import parse
from src.fetch.function import CompoundFunctionData, FunctionData, FunctionType, FunctionOOP, FunctionDoc, ListType, \
    FunctionUrl, FunctionArgument

url_placeholder = FunctionUrl(url='U', name='N', category='C', function_type=ListType.CLIENT)


@pytest.mark.parametrize(
    'code,expected',
    [
        [
            """__NOTOC__
{{Client function}}
This function retrieves the local screen size according to the resolution they are using.

==Syntax== 
<syntaxhighlight lang="lua">
float float guiGetScreenSize()
</syntaxhighlight>
{{OOP||[[GUI widgets|GuiElement]].getScreenSize||}}

===Returns===
This returns two floats representing the player's screen resolution, ''width'' and ''height''.

==Example== 
This example checks whether a player is using a low resolution, and warns them that GUI may appear incorrect.
<syntaxhighlight lang="lua">
--setup a function when the resource starts
function checkResolutionOnStart ()
    local x,y = guiGetScreenSize() --get their screen size
    if ( x <= 640 ) and ( y <= 480 ) then --if their resolution is lower or equal to 640x480
        --warn them about GUI problems.
        outputChatBox ( "WARNING: You are running on a low resolution.  Some GUI may be placed or appear incorrectly." )
    end
end
--attach the function to the event handler
addEventHandler ( "onClientResourceStart", resourceRoot, checkResolutionOnStart )
</syntaxhighlight>


==Using guiGetScreenSize to fit GUI & DX drawing in all resolutions==
To get the precise coordinates of a GUI element or DX drawings, you need to decide which edges of the screen you want to have them positioned against, then you just need to find the difference between your screen size and your position values.

For example, there is a DX text. It fits on 1024x768 resolution.
<syntaxhighlight lang="lua">
function DXtext ()
dxDrawText(tostring "Hello World!",684.0,731.0,732.0,766.0,tocolor(0,255,255,175),1.0,"bankgothic","left","top",false,false,false)
end

addEventHandler ( "onClientRender", getRootElement(), DXtext )
</syntaxhighlight>
Now if you want it to fit on all resolutions. Then follow these steps:

1. Add ''width'' and ''height'' variables to get GUI's screen size, here we use sWidth and sHeight.
<syntaxhighlight lang="lua">
local sWidth,sHeight = guiGetScreenSize() -- The variables
dxDrawText( "Hello World!",684.0,731.0,732.0,766.0,tocolor(0,255,255,175),1.0,"bankgothic","left","top",false,false,false)
</syntaxhighlight>

2. Divide each of the DX text's position values by the screen size manually (remembering the resolution is 1024x768):

*'''Left''' position value is 684, 684/1024 = 0.668
*'''Top''' position value is 731, 731/768 = 0.952
*'''Right''' position values is 732, 732/1024 = 0.715
*'''Bottom''' position value is 766, 766/768 = 0.997

You may want to use a calculator to help you count.

3. Now with the answer above remove all of the position values and replace it with the width or height variable multiplied by the answer. Which would be:
<syntaxhighlight lang="lua">
local sWidth,sHeight = guiGetScreenSize() -- The variables
dxDrawText("Hello World!",sWidth*0.668, sHeight*0.952, sWidth*0.715, sHeight*0.997,tocolor(0,255,255,175),1.0,"bankgothic","left","top",false,false,false)
</syntaxhighlight>

So the final results will be a DX text which will fit on all resolutions which will be:
<syntaxhighlight lang="lua">
function DXtext ()
local sWidth,sHeight = guiGetScreenSize() -- The variables
dxDrawText("Hello World!",sWidth*0.668, sHeight*0.952, sWidth*0.715, sHeight*0.997,tocolor(0,255,255,175),1.0,"bankgothic","left","top",false,false,false)
end

addEventHandler ( "onClientRender", getRootElement(), DXtext )
</syntaxhighlight>

We can also do it by ourself doing some calculations in the code. This works in all resolution, adjusting the scale to all screen-sizes.
<syntaxhighlight lang="lua">
local sx, sy = guiGetScreenSize( )

addEventHandler( "onClientRender", root,
    function( )
         dxDrawText( "Hello World!", sx*( 684/1024 ), sy*( 731/768 ), sx*( 732/1024 ), sy*( 766/768 ), tocolor(0,255,255,175), sx/1000*1.0,"bankgothic","left","top",false,false,false ) 
    end
)
</syntaxhighlight>

==See Also==
{{GUI_functions}}
{{GUI_events}}
""",
            CompoundFunctionData(server=None,
                                 client=FunctionData(
                                     signature=FunctionType(name='guiGetScreenSize',
                                                            return_types=['float', 'float'],
                                                            arguments=[]),
                                     docs=FunctionDoc(
                                         description='This function retrieves the local screen size according to the resolution they are using.',
                                         arguments={},
                                         result="This returns two floats representing the player's screen resolution, ''width'' and ''height''."),
                                     oop=FunctionOOP(class_name='GuiElement',
                                                     method_name='getScreenSize',
                                                     field=None),
                                     url=url_placeholder)),
        ],
        [
            """__NOTOC__ 
{{Client function}}
This function gets the given radio channel name.

==Syntax== 
<syntaxhighlight lang="lua">
string getRadioChannelName ( int id )             
</syntaxhighlight> 

===Required Arguments=== 
*'''id:''' The ID of the radio station you want to get the name of. It is a number from 0 to 12.
{{SoundID}}

===Returns===
Returns a string containing the station name if successful, ''false'' otherwise.

==Example==
<section name="Client" class="client" show="true">
<syntaxhighlight lang="lua">
addCommandHandler("getradio",
    function()
        outputChatBox("You're currently listening to "..getRadioChannelName(getRadioChannel()).."!")
    end
)
</syntaxhighlight>
</section>

==See Also==

{{Client_audio_functions}}
[[HU:GetRadioChannelName]]
[[AR:getRadioChannelName]]
[[RU:GetRadioChannelName]]
[[PL:GetRadioChannelName]]
[[RO:GetRadioChannelName]]
""",
            CompoundFunctionData(server=None,
                                 client=FunctionData(
                                     signature=FunctionType(name='getRadioChannelName',
                                                            return_types=['string'],
                                                            arguments=[
                                                                FunctionArgument(name='id',
                                                                                 argument_type='int',
                                                                                 default_value=None,
                                                                                 optional=False)]),
                                     docs=FunctionDoc(description='This function gets the given radio channel name.',
                                                      arguments={
                                                          'id': 'The ID of the radio station you want to get the name of. It is a number from 0 to 12.\n{{SoundID}}'},
                                                      result="Returns a string containing the station name if successful, ''false'' otherwise."),
                                     oop=None,
                                     url=url_placeholder))
        ],
        [
            """__NOTOC__ 
{{Client function}}
This function is used to get the pan level of the specified [[sound]] element.

==Syntax== 
<syntaxhighlight lang="lua">float getSoundPan ( element theSound )</syntaxhighlight> 
{{OOP||[[sound]]:getPan|pan|setSoundPan}}
===Required Arguments=== 
*'''theSound:''' the [[sound]] element which pan you want to get.

===Returns===
Returns ''float'' value with range from ''-1.0 (left)'' to ''1.0 (right)'', ''false'' otherwise.

==Example== 
<section name="Client" class="client" show="true">
<syntaxhighlight lang="lua">
function playMusic()
    local song = playSound("song.mp3")
    setSoundPan(song, 0.3)
    outputChatBox("Current pan is " .. getSoundPan(song))
end
addCommandHandler("music", playMusic)
</syntaxhighlight>
</section>

==See Also==
{{Client_audio_functions}}

[[AR:getSoundPan]]
[[HU:getSoundPan]]
""",
            CompoundFunctionData(server=None,
                                 client=FunctionData(
                                     signature=FunctionType(name='getSoundPan',
                                                            return_types=['float'],
                                                            arguments=[
                                                                FunctionArgument(name='theSound',
                                                                                 argument_type='element',
                                                                                 default_value=None,
                                                                                 optional=False)]),
                                     docs=FunctionDoc(
                                         description='This function is used to get the pan level of the specified [[sound]] element.',
                                         arguments={'theSound': 'the sound element which pan you want to get.'},
                                         result="Returns ''float'' value with range from ''-1.0 (left)'' to ''1.0 (right)'', ''false'' otherwise."),
                                     oop=FunctionOOP(class_name='sound',
                                                     method_name='getPan',
                                                     field='pan'),
                                     url=url_placeholder))
        ],
        [
            """__NOTOC__
{{Client function}}
{{New feature/item|3.0150|1.5||
This function loads the specified URL.
{{Note|You should use [[requestBrowserDomains]] first to request permission to load the url on the client.}}
{{Note|Calling loadBrowserURL right after [[createBrowser]] will not work normally due to the nature of the asynchronous browser interface. Refer to [[onClientBrowserCreated]] for more information.}}
}}

==Syntax==
<syntaxhighlight lang="lua">bool loadBrowserURL ( browser webBrowser, string url [, string postData = "", bool urlEncoded = true ] )</syntaxhighlight>
{{OOP||[[Element/Browser|browser]]:loadURL|url|getBrowserURL}}

===Required arguments===
*'''webBrowser:''' The [[Element/Browser|browser]] element which will load the URL
*'''url:''' The url you want to load. It can either contain a remote website ("http://" prefix) or a website stored within a local resource ("http://mta/local/gui.html" for example, see [[Local_Scheme_Handler|Local Scheme Handler]] for details).

===Optional Arguments===
*'''postData:''' The post data passed to the website. Its content type can be any type (e.g. JSON) if urlEncoded is set to ''false''
*'''urlEncoded:''' If set to ''true'', it will be available f.e. in PHP's $_POST variable (the content type is: ''application/x-www-form-urlencoded'')

===Returns===
Returns ''true'' if the URL was successfully loaded.

==Example==
<syntaxhighlight lang="lua">
-- In order to render the browser on the full screen, we need to know the dimensions.
local screenWidth, screenHeight = guiGetScreenSize()

-- Let's create a new browser in local mode. We will not be able to load an external URL.
local webBrowser = createBrowser(screenWidth, screenHeight, false, false)
    
-- This is the function to render the browser.
function webBrowserRender()
    -- Render the browser on the full size of the screen.
    dxDrawImage(0, 0, screenWidth, screenHeight, webBrowser, 0, 0, 0, tocolor(255,255,255,255), true)
end

-- The event onClientBrowserCreated will be triggered, after the browser has been initialized.
-- After this event has been triggered, we will be able to load our URL and start drawing.
addEventHandler("onClientBrowserCreated", webBrowser, 
    function()
        -- After the browser has been initialized, we can load our website.
        loadBrowserURL(webBrowser, "https://www.youtube.com/")

        -- Now we can start to render the browser.
        addEventHandler("onClientRender", root, webBrowserRender)
    end
)
</syntaxhighlight>

==See also==
{{CEF_functions}}

[[hu:loadBrowserURL]]
[[RO:loadBrowserURL]]
""",
            CompoundFunctionData(server=None, client=FunctionData(
                signature=FunctionType(name='loadBrowserURL',
                                       return_types=['bool'],
                                       arguments=[
                                           FunctionArgument(name='webBrowser',
                                                            argument_type='browser',
                                                            default_value=None,
                                                            optional=False),
                                           FunctionArgument(name='url',
                                                            argument_type='string', default_value=None,
                                                            optional=False),
                                           FunctionArgument(name='postData',
                                                            argument_type='string',
                                                            default_value='""',
                                                            optional=True),
                                           FunctionArgument(name='urlEncoded',
                                                            argument_type='bool',
                                                            default_value='true',
                                                            optional=True)]),
                docs=FunctionDoc(description='This function loads the specified URL.\n}}',
                                 arguments={'webBrowser': 'The Element/Browser|browser element which will load the URL',
                                            'url': 'The url you want to load. It can either contain a remote website (http:// prefix) or a website stored within a local resource (http://mta/local/gui.html for example, see Local_Scheme_Handler|Local Scheme Handler for details).',
                                            'postData': 'The post data passed to the website. Its content type can be any type (e.g. JSON) if urlEncoded is set to false',
                                            'urlEncoded': 'If set to true, it will be available f.e. in PHPs $_POST variable (the content type is: application/x-www-form-urlencoded)'},
                                 result="Returns ''true'' if the URL was successfully loaded."),
                oop=FunctionOOP(class_name='browser',
                                method_name='loadURL',
                                field=None),
                url=url_placeholder))
        ],
    ],
)
def test_parse_gui_get_screen_size(code, expected):
    result = parse(code, url_placeholder)

    assert result == expected
