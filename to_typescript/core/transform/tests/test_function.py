import pytest

from crawler.core.types import PageUrl, ListType
from to_python.core.types import FunctionType, \
    FunctionArgument, \
    FunctionArgumentValues, \
    FunctionReturnTypes, \
    FunctionSignature, \
    FunctionDoc, \
    FunctionData
from to_typescript.core.transform.function import TypeScriptFunctionGenerator


@pytest.fixture
def function_generator_fixture() -> TypeScriptFunctionGenerator:
    data = FunctionData(
        signature=FunctionSignature(
            name='getZoneName',
            return_types=FunctionReturnTypes(
                return_types=[
                    FunctionType(
                        names=['string', 'mixed'],
                        is_optional=True,
                    ),
                    FunctionType(
                        names=['int'],
                        is_optional=False,
                    ),
                ],
                variable_length=True,
            ),
            arguments=FunctionArgumentValues(
                arguments=[
                    [
                        FunctionArgument(
                            name='x',
                            argument_type=FunctionType(
                                names=['float'],
                                is_optional=False,
                            ),
                            default_value=None,
                        )
                    ],
                    [
                        FunctionArgument(
                            name='y',
                            argument_type=FunctionType(
                                names=['float'],
                                is_optional=False,
                            ),
                            default_value=None,
                        )
                    ],
                    [
                        FunctionArgument(
                            name='z',
                            argument_type=FunctionType(
                                names=['float'],
                                is_optional=False,
                            ),
                            default_value=None,
                        ),
                        FunctionArgument(
                            name='z_1',
                            argument_type=FunctionType(
                                names=['string'],
                                is_optional=False,
                            ),
                            default_value=None,
                        ),
                    ],
                    [
                        FunctionArgument(
                            name='citiesonly',
                            argument_type=FunctionType(
                                names=['bool'],
                                is_optional=True,
                            ),
                            default_value='false',
                        )
                    ]
                ],
                variable_length=True,
            ),
        ),
        url='getZoneName',
        docs=FunctionDoc(
            description="""This function allows you to retrieve the zone name of a certain location. """,
            arguments={
                "x": """The X axis position """,
                "y": """The Y axis position """,
                "z": """The Z axis position """,
                "citiesonly": """: An optional argument to choose if you want to return one of the following city names:
** Tierra Robada
** Bone County
** Las Venturas
** San Fierro
** Red County
** Whetstone
** Flint County
** Los Santos """
            },
            result="""returns the string of the zone name """,
        ),
    )
    url = PageUrl(
        url="/wiki/GetZoneName",
        name="getZoneName",
        category="World functions",
        type=ListType.SERVER,
    )

    return TypeScriptFunctionGenerator(data=data, url=url, host_name='https://example.com')


def test_function_cut_doc_lines():
    code = f'''<!-- Describe in plain english what this function does. Don't go into details, just give an overview -->

This function adds the given ACL to the given ACL group. This makes the resources and players in the given ACL group have access to what's specified in the given ACL. The rights for something in the different ACL's in a group are OR-ed together, which means if one ACL gives access to something, this ACL group will have access to that.
'''
    expected = f'''<!-- Describe in plain english what this function does. Don't go into details, just give
 * an overview -->
 * This function adds the given ACL to the given ACL group. This makes the resources and
 * players in the given ACL group have access to what's specified in the given ACL. The
 * rights for something in the different ACL's in a group are OR-ed together, which means if
 * one ACL gives access to something, this ACL group will have access to that.'''

    result = TypeScriptFunctionGenerator.cut_doc_lines(code)
    assert result == expected


def test_function_generate_doc(function_generator_fixture: TypeScriptFunctionGenerator):
    expected = '''
 * This function allows you to retrieve the zone name of a certain location.
 * @see https://example.com/wiki/GetZoneName
 * @param x The X axis position
 * @param y The Y axis position
 * @param z The Z axis position
 * @param citiesonly : An optional argument to choose if you want to return one of the following city names:
 * ** Tierra Robada
 * ** Bone County
 * ** Las Venturas
 * ** San Fierro
 * ** Red County
 * ** Whetstone
 * ** Flint County
 * ** Los Santos
 * @return returns the string of the zone name
'''
    docs = function_generator_fixture.generate_doc()

    assert docs == expected


def test_function_generate_doc_no_return(function_generator_fixture: TypeScriptFunctionGenerator):
    function_generator_fixture.data.docs.result = '  \n '

    expected = '''
 * This function allows you to retrieve the zone name of a certain location.
 * @see https://example.com/wiki/GetZoneName
 * @param x The X axis position
 * @param y The Y axis position
 * @param z The Z axis position
 * @param citiesonly : An optional argument to choose if you want to return one of the following city names:
 * ** Tierra Robada
 * ** Bone County
 * ** Las Venturas
 * ** San Fierro
 * ** Red County
 * ** Whetstone
 * ** Flint County
 * ** Los Santos
'''
    docs = function_generator_fixture.generate_doc()

    assert docs == expected


def test_function_generate_doc_no_args(function_generator_fixture: TypeScriptFunctionGenerator):
    function_generator_fixture.data.docs.arguments = dict()

    expected = '''
 * This function allows you to retrieve the zone name of a certain location.
 * @see https://example.com/wiki/GetZoneName
 * @return returns the string of the zone name
'''
    docs = function_generator_fixture.generate_doc()

    assert docs == expected


def test_function_generate_return_type_multiple(function_generator_fixture: TypeScriptFunctionGenerator):
    expected = '''LuaMultiReturn<[
    string | mixed | undefined,
    int,
    ...any[]
]>'''
    result = function_generator_fixture.generate_return_type()

    assert result == expected


def test_function_generate_return_type_single(function_generator_fixture: TypeScriptFunctionGenerator):
    function_generator_fixture.data.signature.return_types.return_types = \
        function_generator_fixture.data.signature.return_types.return_types[:1]
    function_generator_fixture.data.signature.return_types.variable_length = False
    expected = '''string | mixed | undefined'''
    result = function_generator_fixture.generate_return_type()

    assert result == expected


def test_function_generate_return_type_void(function_generator_fixture: TypeScriptFunctionGenerator):
    function_generator_fixture.data.signature.return_types.return_types = []
    function_generator_fixture.data.signature.return_types.variable_length = False
    expected = '''void'''
    result = function_generator_fixture.generate_return_type()

    assert result == expected


def test_function_generate_arg_text():
    arg = [
        FunctionArgument(
            name='z',
            argument_type=FunctionType(
                names=['float'],
                is_optional=True,
            ),
            default_value=None,
        ),
        FunctionArgument(
            name='z_1',
            argument_type=FunctionType(
                names=['string'],
                is_optional=False,
            ),
            default_value='aasdasd',
        ),
    ]
    expected = 'z?: float | string'
    result = TypeScriptFunctionGenerator.function_arg_text(arg)

    assert result == expected


def test_function_generate_arguments(function_generator_fixture: TypeScriptFunctionGenerator):
    expected = f'''x: float,
    y: float,
    z: float | string,
    citiesonly?: bool,
    ...varargs: any[]'''
    result = function_generator_fixture.generate_arguments(function_generator_fixture.data.signature.arguments)

    assert result == expected


def test_function_generate_arguments_last_varargs_cut(function_generator_fixture: TypeScriptFunctionGenerator):
    function_generator_fixture.data.signature.arguments.arguments.append(
        [
            FunctionArgument(name='arguments',
                             argument_type=FunctionType(
                                 names=['var'],
                                 is_optional=True
                             ),
                             default_value=None, )
        ]
    )
    expected = f'''x: float,
    y: float,
    z: float | string,
    citiesonly?: bool,
    ...varargs: any[]'''
    result = function_generator_fixture.generate_arguments(function_generator_fixture.data.signature.arguments)

    assert result == expected


def test_function_generate_arguments_no_args(function_generator_fixture: TypeScriptFunctionGenerator):
    function_generator_fixture.data.signature.arguments.arguments = []
    function_generator_fixture.data.signature.arguments.variable_length = False
    expected = ''
    result = function_generator_fixture.generate_arguments(function_generator_fixture.data.signature.arguments)

    assert result == expected


def test_function_generate_full(function_generator_fixture: TypeScriptFunctionGenerator):
    expected = '''/**
 * This function allows you to retrieve the zone name of a certain location.
 * @see https://example.com/wiki/GetZoneName
 * @param x The X axis position
 * @param y The Y axis position
 * @param z The Z axis position
 * @param citiesonly : An optional argument to choose if you want to return one of the following city names:
 * ** Tierra Robada
 * ** Bone County
 * ** Las Venturas
 * ** San Fierro
 * ** Red County
 * ** Whetstone
 * ** Flint County
 * ** Los Santos
 * @return returns the string of the zone name
 * @noSelf
 */
export declare function getZoneName(
    x: float,
    y: float,
    z: float | string,
    citiesonly?: bool,
    ...varargs: any[]
): LuaMultiReturn<[
    string | mixed | undefined,
    int,
    ...any[]
]>;'''
    result = function_generator_fixture.generate()

    assert result == expected


def test_function_generate_empty_docs(function_generator_fixture: TypeScriptFunctionGenerator):
    """
    Real case: setTrafficLightState
    """
    function_generator_fixture.data.docs.arguments = dict(x='')
    function_generator_fixture.data.docs.description = ''
    function_generator_fixture.data.docs.result = ''
    expected = '''
 * @see https://example.com/wiki/GetZoneName
 * @param x
'''
    result = function_generator_fixture.generate_doc()

    assert result == expected


def test_function_generate_trailing_whitespace_docs(function_generator_fixture: TypeScriptFunctionGenerator):
    """
    Real case: setWeaponAmmo
    """
    function_generator_fixture.data.docs.arguments = dict(ammoInClip='The amount of ammo to set in the players clip.  '
                                                                     'This will be taken from the main ammo.  '
                                                                     'If left unspecified or set to 0,'
                                                                     ' the current clip will remain.')
    function_generator_fixture.data.docs.description = ''
    function_generator_fixture.data.docs.result = ''
    expected = '''
 * @see https://example.com/wiki/GetZoneName
 * @param ammoInClip The amount of ammo to set in the players clip.  This will be taken from the main ammo.
 * If left unspecified or set to 0, the current clip will remain.
'''
    result = function_generator_fixture.generate_doc()

    assert result == expected
