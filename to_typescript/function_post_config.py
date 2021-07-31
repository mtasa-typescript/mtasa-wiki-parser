from typing import Callable

from to_python.core.types import FunctionArgument, FunctionType, FunctionGeneric
from to_typescript.filters.processing_post import FilterDumpProcessPost, ListType


def register_post_process(function: Callable[[FilterDumpProcessPost], None]) \
        -> Callable[[FilterDumpProcessPost], None]:
    """
    Decorator
    Registers post_process
    """
    apply_post_process.function_list.append(function)
    return function


def apply_post_process(processor: FilterDumpProcessPost):
    for function in apply_post_process.function_list:
        function(processor)


apply_post_process.function_list = []


# Configure here

@register_post_process
def fetch_remote(processor: FilterDumpProcessPost):
    processor.replace_signature_argument(
        ListType.SHARED,
        'fetchRemote',
        'callbackFunction',
        [FunctionArgument(
            name='callbackFunction',
            argument_type=FunctionType(
                names=['FetchRemoteCallback'],
                is_optional=False
            ),
            default_value=None,
        )]
    )


@register_post_process
def add_event_handler(processor: FilterDumpProcessPost):
    processor.replace_signature_argument(
        ListType.SHARED,
        'addEventHandler',
        'handlerFunction',
        [FunctionArgument(
            name='handlerFunction',
            argument_type=FunctionType(
                names=['CallbackType["function"]'],
                is_optional=False
            ),
            default_value=None,
        )]
    )
    processor.replace_signature_argument(
        ListType.SHARED,
        'addEventHandler',
        'eventName',
        [FunctionArgument(
            name='eventName',
            argument_type=FunctionType(
                names=['CallbackType["name"]'],
                is_optional=False
            ),
            default_value=None,
        )]
    )
    processor.add_generic_type(
        ListType.SHARED,
        'addEventHandler',
        FunctionGeneric(
            name='CallbackType',
            extends='GenericEventHandler',
            default_value='GenericEventHandler'
        )
    )


@register_post_process
def remove_event_handler(processor: FilterDumpProcessPost):
    processor.replace_signature_argument(
        ListType.SHARED,
        'removeEventHandler',
        'eventName',
        [FunctionArgument(
            name='eventName',
            argument_type=FunctionType(
                names=['CallbackType["name"]'],
                is_optional=False
            ),
            default_value=None,
        )]
    )
    processor.replace_signature_argument(
        ListType.SHARED,
        'removeEventHandler',
        'functionVar',
        [FunctionArgument(
            name='functionVar',
            argument_type=FunctionType(
                names=['CallbackType["function"]'],
                is_optional=False
            ),
            default_value=None,
        )]
    )

    processor.add_generic_type(
        ListType.SHARED,
        'removeEventHandler',
        FunctionGeneric(
            name='CallbackType',
            extends='GenericEventHandler',
            default_value='GenericEventHandler'
        )
    )


@register_post_process
def trigger_event(processor: FilterDumpProcessPost):
    processor.set_signature_variable_length(
        ListType.SHARED,
        'triggerEvent',
        False,
    )
    processor.remove_signature_argument(
        ListType.SHARED,
        'triggerEvent',
        'argument1',
    )
    processor.replace_signature_argument(
        ListType.SHARED,
        'triggerEvent',
        'eventName',
        [FunctionArgument(
            name='eventName',
            argument_type=FunctionType(
                names=['CallbackType["name"]'],
                is_optional=False
            ),
            default_value=None,
        )]
    )
    processor.add_signature_argument(
        ListType.SHARED,
        'triggerEvent',
        [FunctionArgument(
            name='...args',
            argument_type=FunctionType(
                names=['Parameters<CallbackType["function"]>'],
                is_optional=False
            ),
            default_value=None,
        )]
    )
    processor.add_generic_type(
        ListType.SHARED,
        'triggerEvent',
        FunctionGeneric(
            name='CallbackType',
            extends='GenericEventHandler',
            default_value='GenericEventHandler'
        )
    )


@register_post_process
def trigger_latent_server_event(processor: FilterDumpProcessPost):
    processor.set_signature_variable_length(
        ListType.CLIENT,
        'triggerLatentServerEvent',
        False,
    )
    processor.remove_signature_argument(
        ListType.CLIENT,
        'triggerLatentServerEvent',
        'arguments',
    )
    processor.replace_signature_argument(
        ListType.CLIENT,
        'triggerLatentServerEvent',
        'event',
        [FunctionArgument(
            name='event',
            argument_type=FunctionType(
                names=['CallbackType["name"]'],
                is_optional=False
            ),
            default_value=None,
        )]
    )
    processor.add_signature_argument(
        ListType.CLIENT,
        'triggerLatentServerEvent',
        [FunctionArgument(
            name='...args',
            argument_type=FunctionType(
                names=['Parameters<CallbackType["function"]>'],
                is_optional=False
            ),
            default_value=None,
        )]
    )
    processor.add_generic_type(
        ListType.CLIENT,
        'triggerLatentServerEvent',
        FunctionGeneric(
            name='CallbackType',
            extends='GenericEventHandler',
            default_value='GenericEventHandler'
        )
    )


@register_post_process
def trigger_server_event(processor: FilterDumpProcessPost):
    processor.set_signature_variable_length(
        ListType.CLIENT,
        'triggerServerEvent',
        False,
    )
    processor.remove_signature_argument(
        ListType.CLIENT,
        'triggerServerEvent',
        'arguments',
    )
    processor.replace_signature_argument(
        ListType.CLIENT,
        'triggerServerEvent',
        'event',
        [FunctionArgument(
            name='event',
            argument_type=FunctionType(
                names=['CallbackType["name"]'],
                is_optional=False
            ),
            default_value=None,
        )]
    )
    processor.add_signature_argument(
        ListType.CLIENT,
        'triggerServerEvent',
        [FunctionArgument(
            name='...args',
            argument_type=FunctionType(
                names=['Parameters<CallbackType["function"]>'],
                is_optional=False
            ),
            default_value=None,
        )]
    )
    processor.add_generic_type(
        ListType.CLIENT,
        'triggerServerEvent',
        FunctionGeneric(
            name='CallbackType',
            extends='GenericEventHandler',
            default_value='GenericEventHandler'
        )
    )


@register_post_process
def trigger_latent_server_event(processor: FilterDumpProcessPost):
    processor.set_signature_variable_length(
        ListType.SERVER,
        'triggerLatentClientEvent',
        False,
    )
    processor.remove_signature_argument(
        ListType.SERVER,
        'triggerLatentClientEvent',
        'arguments',
    )
    processor.replace_signature_argument(
        ListType.SERVER,
        'triggerLatentClientEvent',
        'name',
        [FunctionArgument(
            name='name',
            argument_type=FunctionType(
                names=['CallbackType["name"]'],
                is_optional=False
            ),
            default_value=None,
        )]
    )
    processor.add_signature_argument(
        ListType.SERVER,
        'triggerLatentClientEvent',
        [FunctionArgument(
            name='...args',
            argument_type=FunctionType(
                names=['Parameters<CallbackType["function"]>'],
                is_optional=False
            ),
            default_value=None,
        )]
    )
    processor.add_generic_type(
        ListType.SERVER,
        'triggerLatentClientEvent',
        FunctionGeneric(
            name='CallbackType',
            extends='GenericEventHandler',
            default_value='GenericEventHandler'
        )
    )


@register_post_process
def trigger_server_event(processor: FilterDumpProcessPost):
    processor.set_signature_variable_length(
        ListType.SERVER,
        'triggerClientEvent',
        False,
    )
    processor.remove_signature_argument(
        ListType.SERVER,
        'triggerClientEvent',
        'arguments',
    )
    processor.replace_signature_argument(
        ListType.SERVER,
        'triggerClientEvent',
        'name',
        [FunctionArgument(
            name='name',
            argument_type=FunctionType(
                names=['CallbackType["name"]'],
                is_optional=False
            ),
            default_value=None,
        )]
    )
    processor.add_signature_argument(
        ListType.SERVER,
        'triggerClientEvent',
        [FunctionArgument(
            name='...args',
            argument_type=FunctionType(
                names=['Parameters<CallbackType["function"]>'],
                is_optional=False
            ),
            default_value=None,
        )]
    )
    processor.add_generic_type(
        ListType.SERVER,
        'triggerClientEvent',
        FunctionGeneric(
            name='CallbackType',
            extends='GenericEventHandler',
            default_value='GenericEventHandler'
        )
    )


@register_post_process
def set_timer(processor: FilterDumpProcessPost):
    processor.set_signature_variable_length(
        ListType.SHARED,
        'setTimer',
        False,
    )
    processor.remove_signature_argument(
        ListType.SHARED,
        'setTimer',
        'arguments',
    )
    processor.replace_signature_argument(
        ListType.SHARED,
        'setTimer',
        'theFunction',
        [FunctionArgument(
            name='theFunction',
            argument_type=FunctionType(
                names=['CallbackType'],
                is_optional=False
            ),
            default_value=None,
        )]
    )
    processor.add_signature_argument(
        ListType.SHARED,
        'setTimer',
        [FunctionArgument(
            name='...arguments',
            argument_type=FunctionType(
                names=['Parameters<CallbackType>'],
                is_optional=False
            ),
            default_value=None,
        )]
    )
    processor.add_generic_type(
        ListType.SHARED,
        'setTimer',
        FunctionGeneric(
            name='CallbackType',
            extends='TimerCallbackFunction',
            default_value='TimerCallbackFunction'
        )
    )


@register_post_process
def bind_key(processor: FilterDumpProcessPost):
    processor.set_signature_variable_length(
        ListType.SHARED,
        'bindKey',
        False,
    )
    processor.remove_signature_argument(
        ListType.SHARED,
        'bindKey',
        'arguments',
    )
    processor.replace_signature_argument(
        ListType.SHARED,
        'bindKey',
        'handlerFunction',
        [FunctionArgument(
            name='handlerFunction',
            argument_type=FunctionType(
                names=['CallbackType'],
                is_optional=False
            ),
            default_value=None,
        )]
    )
    processor.replace_signature_argument(
        ListType.SHARED,
        'bindKey',
        'key',
        [FunctionArgument(
            name='key',
            argument_type=FunctionType(
                names=['ControlName', 'KeyName'],
                is_optional=False
            ),
            default_value=None,
        )]
    )
    processor.replace_signature_argument(
        ListType.SHARED,
        'bindKey',
        'keyState',
        [FunctionArgument(
            name='keyState',
            argument_type=FunctionType(
                names=['KeyState'],
                is_optional=False
            ),
            default_value=None,
        )]
    )
    processor.add_signature_argument(
        ListType.SHARED,
        'bindKey',
        [FunctionArgument(
            name='...arguments',
            argument_type=FunctionType(
                names=['Parameters<CallbackType>'],
                is_optional=False
            ),
            default_value=None,
        )]
    )
    processor.add_generic_type(
        ListType.SHARED,
        'bindKey',
        FunctionGeneric(
            name='CallbackType',
            extends='BindKeyCallback',
            default_value='BindKeyCallback'
        )
    )


@register_post_process
def add_command_handler(processor: FilterDumpProcessPost):
    processor.replace_signature_argument(
        ListType.SHARED,
        'addCommandHandler',
        'handlerFunction',
        [FunctionArgument(
            name='handlerFunction',
            argument_type=FunctionType(
                names=['CommandHandler'],
                is_optional=False,
            ),
            default_value=None,
        )]
    )


@register_post_process
def remove_command_handler(processor: FilterDumpProcessPost):
    processor.replace_signature_argument(
        ListType.SHARED,
        'removeCommandHandler',
        'handlerFunction',
        [FunctionArgument(
            name='handlerFunction',
            argument_type=FunctionType(
                names=['CommandHandler'],
                is_optional=True,
            ),
            default_value=None,
        )]
    )
