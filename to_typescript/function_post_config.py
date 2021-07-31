import json
from typing import Dict, Any, List

import yaml
from jsonschema import validate

from to_python.core.types import FunctionGeneric, FunctionType, FunctionArgument
from to_typescript.filters.processing_post import FilterDumpProcessPost, ListType, FilterDumpProcessPostError


def parse_side(side: str) -> ListType:
    return ListType[side.upper()]


def apply_actions(processor: FilterDumpProcessPost,
                  function_name: str,
                  side: ListType,
                  actions: Dict[str, Any]):
    functions = processor.get_functions(side, function_name)

    if 'properties' in actions:
        properties: Dict[str, Any] = actions['properties']

        variable_length = properties.get('variableLength')
        if variable_length is not None:
            for function in functions:
                for declaration in function:
                    declaration.signature.arguments.variable_length = False

            print(f'    Applied variable_length = \u001b[34m{variable_length}\u001b[0m')

    if 'addGeneric' in actions:
        generic_list: List[Dict[str, str]] = actions['addGeneric']
        for generic in generic_list:
            name = generic['name']
            extends = generic.get('extends')
            default = generic.get('default')
            processor.add_generic_type(side,
                                       function_name,
                                       FunctionGeneric(
                                           name=name,
                                           extends=extends,
                                           default_value=default,
                                       ))
            print(f'    Add generic parameter:')
            print(f'        Name: \u001b[34m{name}\u001b[0m')
            print(f'        Extends: \u001b[34m{extends}\u001b[0m')
            print(f'        Default: \u001b[34m{default}\u001b[0m')

    if 'replaceArgument' in actions:
        argument_list: List[Dict[str, Any]] = actions['replaceArgument']
        for argument in argument_list:
            name = argument['name']
            arguments = processor.get_signature_arguments_by_name(side,
                                                                  function_name,
                                                                  name)

            if not arguments:
                raise FilterDumpProcessPostError(f'No arguments found.\n'
                                                 f'Side: {side}, name: {function_name}, argument: {name}')
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
            processor.add_signature_argument(side,
                                             function_name,
                                             [arg])

            print(f'    Add argument:')
            print(f'        Name:  \u001b[34m{arg_name}\u001b[0m')
            print(f'        Extends:  \u001b[34m{arg_default}\u001b[0m')
            print(f'        Type:  \u001b[34m{arg_type}\u001b[0m')

    if 'removeArgument' in actions:
        argument_list: List[Dict[str, Any]] = actions['removeArgument']
        for argument in argument_list:
            arg_name = argument.get('name')
            processor.remove_signature_argument(side,
                                                function_name,
                                                arg_name)

            print(f'    Removed argument  \u001b[34m{arg_name}\u001b[0m')


def apply_post_process(processor: FilterDumpProcessPost):
    print('\nLoading PostProcess config from  \u001b[34mfunction-config.yml\u001b[0m')

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
        print(f'Applying actions to  \u001b[34m{function_name} \u001b[35m({side})\u001b[0m')

        apply_actions(processor,
                      function_name,
                      side,
                      data["actions"], )
        print('')
