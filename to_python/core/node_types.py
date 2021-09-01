import abc
import enum
from typing import Dict, List, Optional


class NodeType(enum.Enum):
    Context = 'Context'
    Identifier = 'Identifier'
    ArgumentIdentifier = 'ArgumentIdentifier'
    Expression = 'Expression'
    FunctionCategoryList = 'FunctionCategoryList'
    FunctionArgumentList = 'FunctionArgumentList'
    GenericArgumentList = 'GenericArgumentList'
    FunctionList = 'FunctionList'
    ClassList = 'ClassList'
    NamespaceList = 'NamespaceList'
    Field = 'Field'
    Function = 'Function'
    Method = 'Method'
    Type = 'Type'
    FunctionArgument = 'FunctionArgument'
    GenericArgument = 'GenericArgument'
    TypeList = 'TypeList'


class NodeSideType(enum.Enum):
    Client = 'Client'
    Server = 'Server'


class NodeFieldModifier(enum.Enum):
    Static = 'Static'


class NodeMethodModifier(enum.Enum):
    Static = 'Static'


class NodeFunctionModifier(enum.Enum):
    Export = 'Export'


class NodeClassPrivacyModifier(enum.Enum):
    Private = 'Private'
    Protected = 'Protected'
    Public = 'Public'


class NodeTypeModifier(enum.Enum):
    Optional = 'Optional'


class Node(metaclass=abc.ABCMeta):
    parent: Optional['Node']
    kind: 'NodeType'


class SideNode(Node, metaclass=abc.ABCMeta):
    side: Dict['NodeSideType', bool]


class ContextNode(SideNode):
    function_children: 'FunctionCategoryListNode'
    class_children: 'ClassListNode'
    namespace_children: 'NamespaceListNode'

    kind = NodeType.Context


class IdentifierNode(Node):
    name: str

    kind = NodeType.Identifier


class ArgumentIdentifierNode(IdentifierNode):
    unpack: bool

    kind = NodeType.ArgumentIdentifier


class ListNode(Node, metaclass=abc.ABCMeta):
    children: List['Node']


class ExpressionListNode(ListNode):
    children: List[Node]

    kind = NodeType.Expression


class FileListNode(ListNode, metaclass=abc.ABCMeta):
    pass


class ArgumentListNode(ListNode, metaclass=abc.ABCMeta):
    pass


class TypeListNode(ListNode):
    children: List['TypeNode']

    kind = NodeType.TypeList


class FunctionArgumentListNode(ArgumentListNode):
    children: List['FunctionArgumentNode']

    kind = NodeType.FunctionArgumentList


class FunctionCategoryListNode(ListNode):
    map: Dict[str, 'FunctionListNode']

    kind = NodeType.FunctionCategoryList


class FunctionListNode(ListNode):
    kind = NodeType.FunctionList


class ClassListNode(ListNode):
    method_children: List[Node]
    field_children: List[Node]

    kind = NodeType.ClassList


class NamespaceListNode(ListNode):
    kind = NodeType.NamespaceList


class FieldNode(Node):
    name: 'IdentifierNode'
    privacy: NodeClassPrivacyModifier
    modifiers: Dict[NodeFieldModifier, bool]

    kind = NodeType.Field


class FunctionNode(Node):
    name: 'IdentifierNode'
    generic: 'TypeListNode'
    argument: 'FunctionArgumentListNode'
    result: 'TypeListNode'

    kind = NodeType.Function


class MethodNode(FunctionNode):
    privacy: NodeClassPrivacyModifier
    modifiers: Dict[NodeMethodModifier, bool]

    kind = NodeType.Method


class TypeNode(Node):
    children: List[IdentifierNode]
    modifiers: Dict[NodeTypeModifier, bool]


class TypeArgumentNode(Node, metaclass=abc.ABCMeta):
    type: TypeNode


class FunctionArgumentNode(TypeArgumentNode):
    name: IdentifierNode
    default: Optional[IdentifierNode]
    neighbours: List['FunctionArgumentNode']


class GenericArgumentNode(TypeArgumentNode):
    pass
