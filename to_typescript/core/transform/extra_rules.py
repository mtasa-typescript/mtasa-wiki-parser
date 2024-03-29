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
        'guibrowser': 'GuiBrowser',
        'guiscrollbar': 'GuiScrollBar',
        'guimemo': 'GuiMemo',
        'guielement': 'GuiElement',
        'guiedit': 'GuiEdit',
        'guiradiobutton': 'GuiRadioButton',
        'guiwindow': 'GuiWindow',
        'guicheckbox': 'GuiCheckbox',
        'font': 'DxFont',
        'engine': 'Engine',
        'guicombobox': 'GuiCombobox',
        'guigridlist': 'GuiGridList',
        'guilabel': 'GuiLabel',
        'guistaticimage': 'GuiStaticImage',
        'guitab': 'GuiTab',
        'guitabpanel': 'GuiTabPanel',
        'guifont': 'GuiFont',
        'material': 'Material',
        'screensource': 'DxScreenSource',
        'dxscreensource': 'DxScreenSource',
        'guibutton': 'GuiButton',
        'sound3d': 'Sound3D',
        'dxrendertarget': 'DxRenderTarget',
        'camera': 'Camera',
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
        'txd': 'EngineTXD',
        'dff': 'EngineDFF',
        'col': 'EngineCOL',
        'ifp': 'EngineIFP',
        'enginetxd': 'EngineTXD',
        'enginedff': 'EngineDFF',
        'enginecol': 'EngineCOL',
        'dxtexture': 'DxTexture',
        'dxshader': 'DxShader',
        'dxfont': 'DxFont',
        'primitivetype': 'PrimitiveType',
        'texture': 'DxTexture',
        'object': 'MTASAObject',
        'rendertarget': 'RenderTarget',
        'shader': 'Shader',
        'sound': 'Sound',
        'objectgroup': 'ObjectGroup',
        'projectile': 'Projectile',
        'queryhandle': 'QueryHandle',
        'xml': 'XML',
        'svg': 'Svg',

        # Primitives
        'int': 'number',
        'float': 'number',
        'double': 'number',
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

        # TODO: see the table
        # https://wiki.multitheftauto.com/wiki/
        # EngineGetObjectGroupPhysicalProperty
        'objectgroup-modifiable': 'string',
    }

    def __init__(self, arg_type: str):
        self.arg_type = arg_type

    def convert(self) -> str:
        return self.TYPE_ALIASES.get(self.arg_type.lower(), self.arg_type)


class ClassInheritance:
    """
    Classes inheritance
    https://wiki.multitheftauto.com/wiki/MTA_Classes
    """
    INHERITANCE = {
        'Player': 'Ped',
        'Ped': 'Element',
        'Vehicle': 'Element',
        'Object': 'Element',
        'Pickup': 'Element',
        'Marker': 'Element',
        'ColShape': 'Element',
        'Blip': 'Element',
        'RadarArea': 'Element',
        'Projectile': None,  # getType override error
        'Team': 'Element',
        'TXD': 'Element',
        'DFF': 'Element',
        'COL': 'Element',
        'Sound': 'Element',
        'Material': 'Element',
        'Font': 'Element',
        'Weapon': 'Element',
        'Camera': 'Element',
        'Effect': 'Element',
        'Browser': 'Element',
        'Light': None,  # getType override error
        'Searchlight': 'Element',
        'Water': 'Element',
        'Texture': 'Material',
        'Shader': 'Material',
        'GuiElement': None,
        'GuiMemo': 'GuiElement',
        'GuiEdit': 'GuiElement',
        'GuiWindow': 'GuiElement',
        'GuiBrowser': 'GuiElement',
        'GuiScrollBar': 'GuiElement',
        'GuiCheckbox': 'GuiElement',
        'GuiCombobox': 'GuiElement',
        'GuiGridList': 'GuiElement',
        'GuiLabel': 'GuiElement',
        'GuiStaticImage': 'GuiElement',
        'GuiTab': 'GuiElement',
        'GuiTabPanel': 'GuiElement',
    }

    def __init__(self, arg_type: str):
        self.arg_type = arg_type

    def get_child(self) -> Optional[str]:
        return self.INHERITANCE.get(self.arg_type, None)


def is_varargs_type(type_name: Optional[FunctionType]) -> bool:
    if type_name is None:
        return True

    if 'var' in [name.lower().strip() for name in type_name.names]:
        return True

    if 'unknown' in [name.lower().strip() for name in type_name.names]:
        return True

    return False
