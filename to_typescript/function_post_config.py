import json
from typing import Dict, Any, List

import yaml
from jsonschema import validate

from crawler.core.types import ListType as CrawlerListType
from to_python.core.types import FunctionGeneric, FunctionType, \
    FunctionArgument, FunctionData, CompoundOOPData
from to_typescript.filters.processing_post import FilterDumpProcessPost, \
    ListType, FilterDumpProcessPostError


class FunctionPostConfigException(Exception):
    pass


def parse_side(side: str) -> ListType:
    return ListType[side.upper()]


def get_oop_functions(oops: List[CompoundOOPData], side: ListType,
                      function_name: str) -> List[List[FunctionData]]:
    original_sides = [
        CrawlerListType[side.name]] if side != ListType.SHARED else [
        CrawlerListType.CLIENT,
        CrawlerListType.SERVER
    ]

    return [
        [data.method]
        for data_list in [
            oop[original_side]
            for oop in oops
            for original_side in original_sides
            if oop[original_side]
            if oop[original_side][0].base_function_name == function_name
        ]
        for data in data_list
        if data.method
    ]


def apply_actions(processor: FilterDumpProcessPost,
                  function_name: str,
                  functions: List[List[FunctionData]],
                  side: ListType,
                  actions: Dict[str, Any]):
    if 'properties' in actions:
        properties: Dict[str, Any] = actions['properties']

        variable_length = properties.get('variableLength')
        if variable_length is not None:
            for function in functions:
                for declaration in function:
                    declaration.signature.arguments.variable_length = False

            print(
                f'    Applied variable_length ='
                f' \u001b[34m{variable_length}\u001b[0m'
            )

    if 'addGeneric' in actions:
        generic_list: List[Dict[str, str]] = actions['addGeneric']
        for generic in generic_list:
            name = generic['name']
            extends = generic.get('extends')
            default = generic.get('default')
            processor.add_generic_type(functions,
                                       FunctionGeneric(
                                           name=name,
                                           extends=extends,
                                           default_value=default,
                                       ))
            print('    Add generic parameter:')
            print(f'        Name: \u001b[34m{name}\u001b[0m')
            print(f'        Extends: \u001b[34m{extends}\u001b[0m')
            print(f'        Default: \u001b[34m{default}\u001b[0m')

    if 'replaceArgument' in actions:
        argument_list: List[Dict[str, Any]] = actions['replaceArgument']
        for argument in argument_list:
            name = argument['name']
            arguments = processor.get_signature_arguments_by_name(functions,
                                                                  name)

            if not arguments:
                raise FilterDumpProcessPostError(
                    'No arguments found.\n'
                    f'Side: {side}, name: '
                    f'{function_name}, argument: {name}'
                )
            argument_data = argument['newArgument']
            for inner_argument in arguments:
                to_replace = inner_argument[0]

                arg_name = argument_data.get('name')
                if arg_name is not None:
                    to_replace.name = arg_name

                arg_default = argument_data.get('default')
                if arg_default is not None:
                    to_replace.default_value = arg_default

                arg_type: Dict[str, Any] = argument_data.get('type')
                if arg_type is not None:
                    arg_type_names = arg_type['names']
                    arg_type_optional = arg_type.get('isOptional')

                    to_replace.argument_type.names = arg_type_names
                    to_replace.argument_type.is_optional = arg_type_optional

            print(f'    Replaced parameter {name}:')
            print(f'        Name: \u001b[34m{arg_name}\u001b[0m')
            print(f'        Extends: \u001b[34m{arg_default}\u001b[0m')
            print(f'        Type: \u001b[34m{arg_type}\u001b[0m')

    if 'addArgument' in actions:
        argument_list: List[Dict[str, Any]] = actions['addArgument']
        for argument in argument_list:
            arg_name = argument.get('name')
            arg_default = argument.get('default')

            arg_type: Dict[str, Any] = argument.get('type', dict())
            f_arg_type = FunctionType(names=['unknown'],
                                      is_optional=False)
            if arg_type is not None:
                arg_type_names = arg_type.get('names', [])
                arg_type_optional = arg_type.get('isOptional')

                f_arg_type = FunctionType(names=arg_type_names,
                                          is_optional=arg_type_optional)

            arg = FunctionArgument(name=arg_name,
                                   argument_type=f_arg_type,
                                   default_value=arg_default)
            processor.add_signature_argument(functions,
                                             [arg])

            print('    Add argument:')
            print(f'        Name:  \u001b[34m{arg_name}\u001b[0m')
            print(f'        Extends:  \u001b[34m{arg_default}\u001b[0m')
            print(f'        Type:  \u001b[34m{arg_type}\u001b[0m')

    if 'removeArgument' in actions:
        argument_list: List[Dict[str, Any]] = actions['removeArgument']
        for argument in argument_list:
            arg_name = argument.get('name')
            processor.remove_signature_argument(side,
                                                functions,
                                                arg_name)

            print(f'    Removed argument  \u001b[34m{arg_name}\u001b[0m')

    if 'replaceReturnType' in actions:
        return_types: List[str] = actions['replaceReturnType']['values']

        for f_inner in functions:
            for f in f_inner:
                f.signature.return_types.return_types = [
                    FunctionType(
                        is_optional=False,
                        names=[value],
                    )
                    for value in return_types
                ]

            print('    Replaced return types\u001b[0m')


def apply_post_process(processor: FilterDumpProcessPost):
    print(
        '\nLoading PostProcess config from '
        '\u001b[34mfunction-config.yml\u001b[0m'
    )

    with open('function-config.yml') as file:
        config = yaml.safe_load(file.read())

    with open('function-config.schema.json') as file:
        schema = json.loads(file.read())

    validate(config, schema)
    print('\u001b[32mConfig validation complete\u001b[0m')
    print(f'Loaded config version:  \u001b[34m{config["version"]}\u001b[0m')

    for data in config["data"]:
        function_name = data["functionName"]
        side = parse_side(data["side"])
        print(
            f'Applying actions to '
            f'\u001b[34m{function_name} \u001b[35m({side})\u001b[0m'
        )

        functions = processor.get_functions(side, function_name)
        if not functions:
            raise FunctionPostConfigException(
                f'No functions found for name {function_name}')

        apply_actions(processor=processor,
                      function_name=function_name,
                      functions=functions,
                      side=side,
                      actions=data["actions"], )
        print('')

        if data.get('includeOOP', False):
            print(
                f'Applying actions to OOP with base name '
                f'\u001b[34m{function_name} \u001b[35m({side})\u001b[0m'
            )
            functions = get_oop_functions(processor.context.oops, side,
                                          function_name)
            if not functions:
                raise FunctionPostConfigException(
                    f'No OOP functions found for name {function_name}')

            apply_actions(processor=processor,
                          function_name=function_name,
                          functions=functions,
                          side=side,
                          actions=data["actions"], )
            print('')
