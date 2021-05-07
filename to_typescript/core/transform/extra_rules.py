from typing import Optional

from to_python.core.types import FunctionType


class TypeConverter:
    """
    Converts MTASA Wiki types into TypeScript types
    """

    TYPE_ALIASES = {
        # Classes
        'gui-browser': 'GuiBrowser',
        'gui-scrollbar': 'GuiScrollBar',
        'gui-memo': 'GuiMemo',
        'gui-element': 'GuiElement',
        'gui-edit': 'GuiEdit',
        'gui-window': 'GuiWindow',
        'matrix': 'Matrix',
        'account': 'Account',
        'acl': 'ACL',
        'aclgroup': 'ACLGroup',
        'player': 'Player',
        'table': 'LuaTable',
        'ban': 'Ban',
        'blip': 'Blip',
        'colshape': 'ColShape',
        'element': 'Element',
        'ped': 'Ped',
        'pickup': 'Pickup',
        'resource': 'Resource',
        'team': 'Team',
        'textdisplay': 'TextDisplay',
        'vehicle': 'Vehicle',
        'xmlnode': 'XmlNode',
        'textitem': 'TextItem',
        'file': 'File',
        'marker': 'Marker',
        'radararea': 'RadarArea',
        'request': 'Request',
        'userdata': 'Userdata',
        'water': 'Water',
        'timer': 'Timer',
        'browser': 'Browser',
        'progressbar': 'ProgressBar',
        'light': 'Light',
        'effect': 'Effect',
        'gui': 'Gui',
        'searchlight': 'Searchlight',
        'weapon': 'Weapon',
        'txd': 'Txd',
        'dff': 'Dff',
        'col': 'Col',
        'ifp': 'Ifp',
        'primitivetype': 'PrimitiveType',
        'texture': 'Texture',
        'object': 'MTASAObject',
        'rendertarget': 'RenderTarget',
        'shader': 'Shader',
        'sound': 'Sound',
        'objectgroup': 'ObjectGroup',
        'projectile': 'Projectile',

        # Primitives
        'int': 'number',
        'float': 'number',
        'uint': 'number',
        'color': 'number',
        'str': 'string',
        'bool': 'boolean',
        'var': 'unknown',
        'value': 'unknown',
        'nil': 'null',
        'mixed': 'any',
        'function': 'HandleFunction',
        'handle': 'HandleFunction',
        'callback': 'HandleFunction',

        # Utility

        # TODO: see the table https://wiki.multitheftauto.com/wiki/EngineGetObjectGroupPhysicalProperty
        'objectgroup-modifiable': 'string',
    }

    def __init__(self, arg_type: str):
        self.arg_type = arg_type

    def convert(self) -> str:
        return self.TYPE_ALIASES.get(self.arg_type.lower(), self.arg_type)


def is_varargs_type(type_name: Optional[FunctionType]) -> bool:
    if type_name is None:
        return True

    if 'var' in [name.lower().strip() for name in type_name.names]:
        return True

    return False
