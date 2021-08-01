import pytest

from to_python.core.signature import SignatureTokenizer, SignatureParser
from to_python.core.tests.utils import compare_lists
from to_python.core.types import FunctionSignature, FunctionReturnTypes, FunctionType, FunctionArgument, \
    FunctionArgumentValues

TokenType = SignatureTokenizer.TokenType


@pytest.mark.parametrize("code,expected", [
    (
            'bool givePedWeapon ( ped thePed, int weapon [, int ammo=30, bool setAsCurrent=false ] )',
            [
                SignatureTokenizer.Token(type=TokenType.RETURN_TYPE, value='bool'),
                SignatureTokenizer.Token(type=TokenType.FUNCTION_NAME, value='givePedWeapon'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_START, value='('),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='ped'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='thePed'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='int'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='weapon'),
                SignatureTokenizer.Token(type=TokenType.OPTIONAL_START, value='['),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='int'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='ammo'),
                SignatureTokenizer.Token(type=TokenType.EQUAL_SIGN, value='='),
                SignatureTokenizer.Token(type=TokenType.DEFAULT_VALUE, value='30'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='bool'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='setAsCurrent'),
                SignatureTokenizer.Token(type=TokenType.EQUAL_SIGN, value='='),
                SignatureTokenizer.Token(type=TokenType.DEFAULT_VALUE, value='false'),
                SignatureTokenizer.Token(type=TokenType.OPTIONAL_END, value=']'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_END, value=')')
            ]
    ),
    (
            'bool hasElementData ( element theElement, string key [, bool inherit = true] )',
            [
                SignatureTokenizer.Token(type=TokenType.RETURN_TYPE, value='bool'),
                SignatureTokenizer.Token(type=TokenType.FUNCTION_NAME, value='hasElementData'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_START, value='('),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='element'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='theElement'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='string'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='key'),
                SignatureTokenizer.Token(type=TokenType.OPTIONAL_START, value='['),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='bool'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='inherit'),
                SignatureTokenizer.Token(type=TokenType.EQUAL_SIGN, value='='),
                SignatureTokenizer.Token(type=TokenType.DEFAULT_VALUE, value='true'),
                SignatureTokenizer.Token(type=TokenType.OPTIONAL_END, value=']'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_END, value=')')
            ]
    ),
    (
            'bool hasObjectPermissionTo ( string / element theObject, string theAction [, bool defaultPermission = true ] )',
            [
                SignatureTokenizer.Token(type=TokenType.RETURN_TYPE, value='bool'),
                SignatureTokenizer.Token(type=TokenType.FUNCTION_NAME, value='hasObjectPermissionTo'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_START, value='('),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='string'),
                SignatureTokenizer.Token(type=TokenType.TYPE_UNION_SIGN, value='/'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='element'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='theObject'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='string'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='theAction'),
                SignatureTokenizer.Token(type=TokenType.OPTIONAL_START, value='['),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='bool'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='defaultPermission'),
                SignatureTokenizer.Token(type=TokenType.EQUAL_SIGN, value='='),
                SignatureTokenizer.Token(type=TokenType.DEFAULT_VALUE, value='true'),
                SignatureTokenizer.Token(type=TokenType.OPTIONAL_END, value=']'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_END, value=')')
            ]
    ),
    (
            'bool hasElementDataSubscriber ( element theElement, string key, player thePlayer )',
            [
                SignatureTokenizer.Token(type=TokenType.RETURN_TYPE, value='bool'),
                SignatureTokenizer.Token(type=TokenType.FUNCTION_NAME, value='hasElementDataSubscriber'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_START, value='('),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='element'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='theElement'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='string'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='key'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='player'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='thePlayer'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_END, value=')')
            ]

    ),
    (
            'table executeSQLQuery ( string query [, var param1 [, var param2 ... ] ] ) ',
            [
                SignatureTokenizer.Token(type=TokenType.RETURN_TYPE, value='table'),
                SignatureTokenizer.Token(type=TokenType.FUNCTION_NAME, value='executeSQLQuery'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_START, value='('),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='string'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='query'),
                SignatureTokenizer.Token(type=TokenType.OPTIONAL_START, value='['),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='var'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='param1'),
                SignatureTokenizer.Token(type=TokenType.OPTIONAL_START, value='['),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='var'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='param2'),
                SignatureTokenizer.Token(type=TokenType.VARARGS_SIGN, value='...'),
                SignatureTokenizer.Token(type=TokenType.OPTIONAL_END, value=']'),
                SignatureTokenizer.Token(type=TokenType.OPTIONAL_END, value=']'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_END, value=')')
            ]

    ),
    (
            'bool bindKey ( player thePlayer, string key, string keyState, function handlerFunction,  [ var arguments, ... ] )',
            [
                SignatureTokenizer.Token(type=TokenType.RETURN_TYPE, value='bool'),
                SignatureTokenizer.Token(type=TokenType.FUNCTION_NAME, value='bindKey'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_START, value='('),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='player'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='thePlayer'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='string'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='key'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='string'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='keyState'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='function'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='handlerFunction'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.OPTIONAL_START, value='['),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='var'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='arguments'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.VARARGS_SIGN, value='...'),
                SignatureTokenizer.Token(type=TokenType.OPTIONAL_END, value=']'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_END, value=')')
            ]

    ),
    (
            'bool triggerLatentServerEvent ( string event, [int bandwidth=5000, bool persist=false,] element theElement, [arguments...] )',
            [
                SignatureTokenizer.Token(type=TokenType.RETURN_TYPE, value='bool'),
                SignatureTokenizer.Token(type=TokenType.FUNCTION_NAME, value='triggerLatentServerEvent'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_START, value='('),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='string'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='event'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.OPTIONAL_START, value='['),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='int'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='bandwidth'),
                SignatureTokenizer.Token(type=TokenType.EQUAL_SIGN, value='='),
                SignatureTokenizer.Token(type=TokenType.DEFAULT_VALUE, value='5000'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='bool'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='persist'),
                SignatureTokenizer.Token(type=TokenType.EQUAL_SIGN, value='='),
                SignatureTokenizer.Token(type=TokenType.DEFAULT_VALUE, value='false'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.OPTIONAL_END, value=']'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='element'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='theElement'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.OPTIONAL_START, value='['),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='arguments'),
                SignatureTokenizer.Token(type=TokenType.VARARGS_SIGN, value='...'),
                SignatureTokenizer.Token(type=TokenType.OPTIONAL_END, value=']'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_END, value=')')
            ]

    ),
    (
            'bool triggerClientEvent ( [ table/element sendTo = getRootElement(), ] string name, element sourceElement [, arguments... ] )',
            [
                SignatureTokenizer.Token(type=TokenType.RETURN_TYPE, value='bool'),
                SignatureTokenizer.Token(type=TokenType.FUNCTION_NAME, value='triggerClientEvent'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_START, value='('),
                SignatureTokenizer.Token(type=TokenType.OPTIONAL_START, value='['),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='table'),
                SignatureTokenizer.Token(type=TokenType.TYPE_UNION_SIGN, value='/'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='element'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='sendTo'),
                SignatureTokenizer.Token(type=TokenType.EQUAL_SIGN, value='='),
                SignatureTokenizer.Token(type=TokenType.DEFAULT_VALUE, value='getRootElement()'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.OPTIONAL_END, value=']'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='string'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='name'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='element'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='sourceElement'),
                SignatureTokenizer.Token(type=TokenType.OPTIONAL_START, value='['),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='arguments'),
                SignatureTokenizer.Token(type=TokenType.VARARGS_SIGN, value='...'),
                SignatureTokenizer.Token(type=TokenType.OPTIONAL_END, value=']'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_END, value=')')
            ]
    ),
    (
            'table/xmlnode xmlNodeGetChildren ( xmlnode parent, [ int index ] )',
            [
                SignatureTokenizer.Token(type=TokenType.RETURN_TYPE, value='table'),
                SignatureTokenizer.Token(type=TokenType.TYPE_UNION_SIGN, value='/'),
                SignatureTokenizer.Token(type=TokenType.RETURN_TYPE, value='xmlnode'),
                SignatureTokenizer.Token(type=TokenType.FUNCTION_NAME, value='xmlNodeGetChildren'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_START, value='('),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='xmlnode'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='parent'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.OPTIONAL_START, value='['),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='int'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='index'),
                SignatureTokenizer.Token(type=TokenType.OPTIONAL_END, value=']'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_END, value=')')
            ]
    ),
    (
            'string, string getPedAnimation ( ped thePed )',
            [
                SignatureTokenizer.Token(type=TokenType.RETURN_TYPE, value='string'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.RETURN_TYPE, value='string'),
                SignatureTokenizer.Token(type=TokenType.FUNCTION_NAME, value='getPedAnimation'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_START, value='('),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='ped'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='thePed'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_END, value=')')
            ],
    ),
    (
            'pickup createPickup ( float x, float y, float z, int theType, int amount/weapon/model, [ int respawnTime = 30000, int ammo = 50 ] )',
            [
                SignatureTokenizer.Token(type=TokenType.RETURN_TYPE, value='pickup'),
                SignatureTokenizer.Token(type=TokenType.FUNCTION_NAME, value='createPickup'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_START, value='('),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='float'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='x'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='float'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='y'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='float'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='z'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='int'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='theType'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='int'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='amount/weapon/model'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.OPTIONAL_START, value='['),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='int'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='respawnTime'),
                SignatureTokenizer.Token(type=TokenType.EQUAL_SIGN, value='='),
                SignatureTokenizer.Token(type=TokenType.DEFAULT_VALUE, value='30000'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='int'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='ammo'),
                SignatureTokenizer.Token(type=TokenType.EQUAL_SIGN, value='='),
                SignatureTokenizer.Token(type=TokenType.DEFAULT_VALUE, value='50'),
                SignatureTokenizer.Token(type=TokenType.OPTIONAL_END, value=']'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_END, value=')')
            ]
    ),
    (
            'string sampleTestFunction(string value / int theNumber)',
            [
                SignatureTokenizer.Token(type=TokenType.RETURN_TYPE, value='string'),
                SignatureTokenizer.Token(type=TokenType.FUNCTION_NAME, value='sampleTestFunction'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_START, value='('),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='string'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='value'),
                SignatureTokenizer.Token(type=TokenType.TYPE_UNION_SIGN, value='/'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='int'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='theNumber'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_END, value=')')
            ]
    ),
    (
            'table getBoundKeys ( string command/control )',
            [
                SignatureTokenizer.Token(type=TokenType.RETURN_TYPE, value='table'),
                SignatureTokenizer.Token(type=TokenType.FUNCTION_NAME, value='getBoundKeys'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_START, value='('),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='string'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='command/control'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_END, value=')')
            ]
    ),
    (
            'bool setVehiclesLODDistance ( float vehiclesDistance, float trainsAndPlanesDistance = vehiclesDistance * 2.14 )',
            [
                SignatureTokenizer.Token(type=TokenType.RETURN_TYPE, value='bool'),
                SignatureTokenizer.Token(type=TokenType.FUNCTION_NAME, value='setVehiclesLODDistance'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_START, value='('),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='float'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='vehiclesDistance'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='float'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='trainsAndPlanesDistance'),
                SignatureTokenizer.Token(type=TokenType.EQUAL_SIGN, value='='),
                SignatureTokenizer.Token(type=TokenType.DEFAULT_VALUE, value='vehiclesDistance*2.14'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_END, value=')')
            ]
    ),
    (
            'int, int [, int] dxGetMaterialSize ( element material )',
            [
                SignatureTokenizer.Token(type=TokenType.RETURN_TYPE, value='int'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.RETURN_TYPE, value='int'),
                SignatureTokenizer.Token(type=TokenType.OPTIONAL_START, value='['),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.RETURN_TYPE, value='int'),
                SignatureTokenizer.Token(type=TokenType.OPTIONAL_END, value=']'),
                SignatureTokenizer.Token(type=TokenType.FUNCTION_NAME, value='dxGetMaterialSize'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_START, value='('),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='element'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='material'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_END, value=')')
            ]
    ),
    (
            'bool|int|table getChatboxLayout ( [ string CVar ] )',
            [
                SignatureTokenizer.Token(type=TokenType.RETURN_TYPE, value='bool'),
                SignatureTokenizer.Token(type=TokenType.TYPE_UNION_SIGN, value='|'),
                SignatureTokenizer.Token(type=TokenType.RETURN_TYPE, value='int'),
                SignatureTokenizer.Token(type=TokenType.TYPE_UNION_SIGN, value='|'),
                SignatureTokenizer.Token(type=TokenType.RETURN_TYPE, value='table'),
                SignatureTokenizer.Token(type=TokenType.FUNCTION_NAME, value='getChatboxLayout'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_START, value='('),
                SignatureTokenizer.Token(type=TokenType.OPTIONAL_START, value='['),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='string'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='CVar'),
                SignatureTokenizer.Token(type=TokenType.OPTIONAL_END, value=']'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_END, value=')')
            ]
    ),
    (
            'bool dxSetAspectRatioAdjustmentEnabled ( bool bEnabled [, float sourceRatio = 4/3 ] )',
            [
                SignatureTokenizer.Token(type=TokenType.RETURN_TYPE, value='bool'),
                SignatureTokenizer.Token(type=TokenType.FUNCTION_NAME, value='dxSetAspectRatioAdjustmentEnabled'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_START, value='('),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='bool'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='bEnabled'),
                SignatureTokenizer.Token(type=TokenType.OPTIONAL_START, value='['),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='float'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='sourceRatio'),
                SignatureTokenizer.Token(type=TokenType.EQUAL_SIGN, value='='),
                SignatureTokenizer.Token(type=TokenType.DEFAULT_VALUE, value='4/3'),
                SignatureTokenizer.Token(type=TokenType.OPTIONAL_END, value=']'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_END, value=')')
            ]
    ),
    (
            'string utf8.insert ( string input [, int insert_pos = utf8.len( input ) + 1 ], string substring )',
            [
                SignatureTokenizer.Token(type=TokenType.RETURN_TYPE, value='string'),
                SignatureTokenizer.Token(type=TokenType.FUNCTION_NAME, value='utf8.insert'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_START, value='('),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='string'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='input'),
                SignatureTokenizer.Token(type=TokenType.OPTIONAL_START, value='['),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='int'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='insert_pos'),
                SignatureTokenizer.Token(type=TokenType.EQUAL_SIGN, value='='),
                SignatureTokenizer.Token(type=TokenType.DEFAULT_VALUE, value='utf8.len(input)+1'),
                SignatureTokenizer.Token(type=TokenType.OPTIONAL_END, value=']'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='string'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='substring'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_END, value=')')
            ]
    ),
    (
            'table engineGetVisibleTextureNames ( [ string nameFilter = "*", string modelId = "" ] )',
            [
                SignatureTokenizer.Token(type=TokenType.RETURN_TYPE, value='table'),
                SignatureTokenizer.Token(type=TokenType.FUNCTION_NAME, value='engineGetVisibleTextureNames'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_START, value='('),
                SignatureTokenizer.Token(type=TokenType.OPTIONAL_START, value='['),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='string'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='nameFilter'),
                SignatureTokenizer.Token(type=TokenType.EQUAL_SIGN, value='='),
                SignatureTokenizer.Token(type=TokenType.DEFAULT_VALUE, value='"*"'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='string'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='modelId'),
                SignatureTokenizer.Token(type=TokenType.EQUAL_SIGN, value='='),
                SignatureTokenizer.Token(type=TokenType.DEFAULT_VALUE, value='""'),
                SignatureTokenizer.Token(type=TokenType.OPTIONAL_END, value=']'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_END, value=')')
            ]
    ),
    (
            'var... call ( resource theResource, string theFunction, [ arguments... ] )',
            [
                SignatureTokenizer.Token(type=TokenType.RETURN_TYPE, value='var'),
                SignatureTokenizer.Token(type=TokenType.VARARGS_RETURN_SIGN, value='...'),
                SignatureTokenizer.Token(type=TokenType.FUNCTION_NAME, value='call'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_START, value='('),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='resource'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='theResource'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='string'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='theFunction'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.OPTIONAL_START, value='['),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='arguments'),
                SignatureTokenizer.Token(type=TokenType.VARARGS_SIGN, value='...'),
                SignatureTokenizer.Token(type=TokenType.OPTIONAL_END, value=']'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_END, value=')')
            ]
    ),
    (
            'bool float float float element float float float int float int int float float float float float float int processLineOfSight ( float startX, float startY, float startZ, float endX, float endY, float endZ, [ bool checkBuildings = true, bool checkVehicles = true, bool checkPlayers = true, bool checkObjects = true, bool checkDummies = true, bool seeThroughStuff = false, bool ignoreSomeObjectsForCamera = false, bool shootThroughStuff = false, element ignoredElement = nil, bool includeWorldModelInformation = false, bool bIncludeCarTyres ] )',
            [
                SignatureTokenizer.Token(type=TokenType.RETURN_TYPE, value='bool'),
                SignatureTokenizer.Token(type=TokenType.RETURN_TYPE, value='float'),
                SignatureTokenizer.Token(type=TokenType.RETURN_TYPE, value='float'),
                SignatureTokenizer.Token(type=TokenType.RETURN_TYPE, value='float'),
                SignatureTokenizer.Token(type=TokenType.RETURN_TYPE, value='element'),
                SignatureTokenizer.Token(type=TokenType.RETURN_TYPE, value='float'),
                SignatureTokenizer.Token(type=TokenType.RETURN_TYPE, value='float'),
                SignatureTokenizer.Token(type=TokenType.RETURN_TYPE, value='float'),
                SignatureTokenizer.Token(type=TokenType.RETURN_TYPE, value='int'),
                SignatureTokenizer.Token(type=TokenType.RETURN_TYPE, value='float'),
                SignatureTokenizer.Token(type=TokenType.RETURN_TYPE, value='int'),
                SignatureTokenizer.Token(type=TokenType.RETURN_TYPE, value='int'),
                SignatureTokenizer.Token(type=TokenType.RETURN_TYPE, value='float'),
                SignatureTokenizer.Token(type=TokenType.RETURN_TYPE, value='float'),
                SignatureTokenizer.Token(type=TokenType.RETURN_TYPE, value='float'),
                SignatureTokenizer.Token(type=TokenType.RETURN_TYPE, value='float'),
                SignatureTokenizer.Token(type=TokenType.RETURN_TYPE, value='float'),
                SignatureTokenizer.Token(type=TokenType.RETURN_TYPE, value='float'),
                SignatureTokenizer.Token(type=TokenType.RETURN_TYPE, value='int'),
                SignatureTokenizer.Token(type=TokenType.FUNCTION_NAME, value='processLineOfSight'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_START, value='('),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='float'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='startX'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='float'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='startY'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='float'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='startZ'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='float'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='endX'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='float'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='endY'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='float'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='endZ'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.OPTIONAL_START, value='['),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='bool'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='checkBuildings'),
                SignatureTokenizer.Token(type=TokenType.EQUAL_SIGN, value='='),
                SignatureTokenizer.Token(type=TokenType.DEFAULT_VALUE, value='true'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='bool'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='checkVehicles'),
                SignatureTokenizer.Token(type=TokenType.EQUAL_SIGN, value='='),
                SignatureTokenizer.Token(type=TokenType.DEFAULT_VALUE, value='true'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='bool'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='checkPlayers'),
                SignatureTokenizer.Token(type=TokenType.EQUAL_SIGN, value='='),
                SignatureTokenizer.Token(type=TokenType.DEFAULT_VALUE, value='true'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='bool'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='checkObjects'),
                SignatureTokenizer.Token(type=TokenType.EQUAL_SIGN, value='='),
                SignatureTokenizer.Token(type=TokenType.DEFAULT_VALUE, value='true'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='bool'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='checkDummies'),
                SignatureTokenizer.Token(type=TokenType.EQUAL_SIGN, value='='),
                SignatureTokenizer.Token(type=TokenType.DEFAULT_VALUE, value='true'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='bool'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='seeThroughStuff'),
                SignatureTokenizer.Token(type=TokenType.EQUAL_SIGN, value='='),
                SignatureTokenizer.Token(type=TokenType.DEFAULT_VALUE, value='false'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='bool'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='ignoreSomeObjectsForCamera'),
                SignatureTokenizer.Token(type=TokenType.EQUAL_SIGN, value='='),
                SignatureTokenizer.Token(type=TokenType.DEFAULT_VALUE, value='false'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='bool'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='shootThroughStuff'),
                SignatureTokenizer.Token(type=TokenType.EQUAL_SIGN, value='='),
                SignatureTokenizer.Token(type=TokenType.DEFAULT_VALUE, value='false'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='element'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='ignoredElement'),
                SignatureTokenizer.Token(type=TokenType.EQUAL_SIGN, value='='),
                SignatureTokenizer.Token(type=TokenType.DEFAULT_VALUE, value='nil'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='bool'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='includeWorldModelInformation'),
                SignatureTokenizer.Token(type=TokenType.EQUAL_SIGN, value='='),
                SignatureTokenizer.Token(type=TokenType.DEFAULT_VALUE, value='false'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='bool'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='bIncludeCarTyres'),
                SignatureTokenizer.Token(type=TokenType.OPTIONAL_END, value=']'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_END, value=')')
            ]
    ),
    (
            'bool callRemote ( string host[, string queueName = "default" ][, int connectionAttempts = 10, int connectTimeout = 10000 ], string resourceName, string functionName, callback callbackFunction, [ arguments... ] )',
            [
                SignatureTokenizer.Token(type=TokenType.RETURN_TYPE, value='bool'),
                SignatureTokenizer.Token(type=TokenType.FUNCTION_NAME, value='callRemote'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_START, value='('),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='string'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='host'),
                SignatureTokenizer.Token(type=TokenType.OPTIONAL_START, value='['),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='string'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='queueName'),
                SignatureTokenizer.Token(type=TokenType.EQUAL_SIGN, value='='),
                SignatureTokenizer.Token(type=TokenType.DEFAULT_VALUE, value='"default"'),
                SignatureTokenizer.Token(type=TokenType.OPTIONAL_END, value=']'),
                SignatureTokenizer.Token(type=TokenType.OPTIONAL_START, value='['),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='int'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='connectionAttempts'),
                SignatureTokenizer.Token(type=TokenType.EQUAL_SIGN, value='='),
                SignatureTokenizer.Token(type=TokenType.DEFAULT_VALUE, value='10'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='int'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='connectTimeout'),
                SignatureTokenizer.Token(type=TokenType.EQUAL_SIGN, value='='),
                SignatureTokenizer.Token(type=TokenType.DEFAULT_VALUE, value='10000'),
                SignatureTokenizer.Token(type=TokenType.OPTIONAL_END, value=']'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='string'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='resourceName'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='string'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='functionName'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='callback'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='callbackFunction'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.OPTIONAL_START, value='['),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='arguments'),
                SignatureTokenizer.Token(type=TokenType.VARARGS_SIGN, value='...'),
                SignatureTokenizer.Token(type=TokenType.OPTIONAL_END, value=']'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_END, value=')')
            ]
    ),
    (
            'element, string dxCreateShader ( string filepath / string raw_data [, float priority = 0, float maxDistance = 0, bool layered = false, string elementTypes = "world,vehicle,object,other" ] )',
            [
                SignatureTokenizer.Token(type=TokenType.RETURN_TYPE, value='element'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.RETURN_TYPE, value='string'),
                SignatureTokenizer.Token(type=TokenType.FUNCTION_NAME, value='dxCreateShader'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_START, value='('),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='string'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='filepath'),
                SignatureTokenizer.Token(type=TokenType.TYPE_UNION_SIGN, value='/'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='string'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='raw_data'),
                SignatureTokenizer.Token(type=TokenType.OPTIONAL_START, value='['),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='float'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='priority'),
                SignatureTokenizer.Token(type=TokenType.EQUAL_SIGN, value='='),
                SignatureTokenizer.Token(type=TokenType.DEFAULT_VALUE, value='0'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='float'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='maxDistance'),
                SignatureTokenizer.Token(type=TokenType.EQUAL_SIGN, value='='),
                SignatureTokenizer.Token(type=TokenType.DEFAULT_VALUE, value='0'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='bool'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='layered'),
                SignatureTokenizer.Token(type=TokenType.EQUAL_SIGN, value='='),
                SignatureTokenizer.Token(type=TokenType.DEFAULT_VALUE, value='false'),
                SignatureTokenizer.Token(type=TokenType.COMMA_SIGN, value=','),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_TYPE, value='string'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_NAME, value='elementTypes'),
                SignatureTokenizer.Token(type=TokenType.EQUAL_SIGN, value='='),
                SignatureTokenizer.Token(type=TokenType.DEFAULT_VALUE, value='"world,vehicle,object,other"'),
                SignatureTokenizer.Token(type=TokenType.OPTIONAL_END, value=']'),
                SignatureTokenizer.Token(type=TokenType.ARGUMENT_END, value=')')
            ]
    )
])
def test_signature_tokenizer_function(code, expected):
    compare_lists(SignatureTokenizer(code).tokenize(), expected)


@pytest.mark.parametrize("code,expected", [
    (
            'string mixed/texture [,int...] synthetic '
            '( string arg1 / int arg1_1 [, string/float arg2 = something*10 ], [ arguments... ] )',
            FunctionSignature(
                name='synthetic',
                return_types=FunctionReturnTypes(
                    return_types=[
                        FunctionType(
                            names=['string'],
                            is_optional=False,
                        ),
                        FunctionType(
                            names=['mixed', 'texture'],
                            is_optional=False,
                        ),
                        FunctionType(
                            names=['int'],
                            is_optional=True,
                        )
                    ],
                    variable_length=True,
                ),
                arguments=FunctionArgumentValues(
                    arguments=[
                        [
                            FunctionArgument(
                                name='arg1',
                                argument_type=FunctionType(
                                    names=['string'],
                                    is_optional=False,
                                ),
                                default_value=None,
                            ),
                            FunctionArgument(
                                name='arg1_1',
                                argument_type=FunctionType(
                                    names=['int'],
                                    is_optional=False,
                                ),
                                default_value=None,
                            )
                        ],
                        [
                            FunctionArgument(
                                name='arg2',
                                argument_type=FunctionType(
                                    names=['string', 'float'],
                                    is_optional=True,
                                ),
                                default_value='something*10',
                            )
                        ],
                        [
                            FunctionArgument(
                                name='arguments',
                                argument_type=None,
                                default_value=None,
                            )
                        ]
                    ],
                    variable_length=True,
                ),
            )
    ),
    (
            'string synthetic2 ( string arg1 / arg1_1 )',
            FunctionSignature(
                name='synthetic2',
                return_types=FunctionReturnTypes(
                    return_types=[
                        FunctionType(
                            names=['string'],
                            is_optional=False,
                        )
                    ],
                    variable_length=False,
                ),
                arguments=FunctionArgumentValues(
                    arguments=[
                        [
                            FunctionArgument(
                                name='arg1/arg1_1',
                                argument_type=FunctionType(
                                    names=['string'],
                                    is_optional=False,
                                ),
                                default_value=None,
                            )
                        ]
                    ],
                    variable_length=False,
                ),
            )
    ),
    (
            'int guiGridListAddRow ( element gridList [, int/string itemText1, int/string itemText2, ... ] )',
            FunctionSignature(
                name='guiGridListAddRow',
                return_types=FunctionReturnTypes(
                    return_types=[
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
                                name='gridList',
                                argument_type=FunctionType(
                                    names=['element'],
                                    is_optional=False,
                                ),
                                default_value=None,
                            )
                        ],
                        [
                            FunctionArgument(
                                name='itemText1',
                                argument_type=FunctionType(
                                    names=['int', 'string'],
                                    is_optional=True,
                                ),
                                default_value=None,
                            )
                        ],
                        [
                            FunctionArgument(
                                name='itemText2',
                                argument_type=FunctionType(
                                    names=['int', 'string'],
                                    is_optional=True,
                                ),
                                default_value=None,
                            )
                        ]
                    ],
                    variable_length=True,
                ),
            )
    ),
])
def test_signature_parser(code, expected):
    tokenized = SignatureTokenizer(code).tokenize()
    result = SignatureParser(tokenized).parse()

    assert result == expected
