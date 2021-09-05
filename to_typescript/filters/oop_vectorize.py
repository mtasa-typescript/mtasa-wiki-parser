import enum
from typing import List, Optional

from to_python.core.types import FunctionOOP, FunctionOOPField, FunctionData, FunctionType, FunctionArgument
from to_typescript.core.filter import FilterAbstract


class VectorizableType(enum.Enum):
    Vector2D = 'Vector2'
    Vector3D = 'Vector3'
    Vector4D = 'Vector4'
    Matrix = 'Matrix'


class FilterDumpProcessVectorizeOOP(FilterAbstract):
    @staticmethod
    def is_vectorizable_field(oop: FunctionOOP) -> Optional[VectorizableType]:
        if not oop.field:
            return None

        if oop.class_name.lower() in {'element', 'player', 'ped', 'object', 'vehicle', 'camera', 'searchlight'}:
            if oop.field.name.lower() in {'position', 'rotation', 'velocity', 'angularvelocity', 'scale'}:
                return VectorizableType.Vector3D

        if oop.class_name.lower() in {'marker'}:
            if 'target' in oop.method.name.lower():
                return VectorizableType.Vector3D

        if oop.class_name.lower() in {'ped'}:
            if 'target' in oop.method.name.lower():
                return VectorizableType.Vector3D

        if oop.field.name.lower() in {'matrix'}:
            return VectorizableType.Matrix

    @staticmethod
    def is_vectorizable_method_args(oop: FunctionOOP) -> Optional[VectorizableType]:
        if not oop.method:
            return None

        if not oop.method.name.startswith('set'):
            return None

        if oop.class_name.lower() in {'element', 'player', 'ped', 'mtasaobject', 'vehicle', 'camera', 'marker',
                                      'searchlight'}:
            if 'position' in oop.method.name.lower() \
                    or 'rotation' in oop.method.name.lower() \
                    or 'velocity' in oop.method.name.lower():
                return VectorizableType.Vector3D

        if oop.class_name.lower() in {'mtasaobject'}:
            if 'scale' in oop.method.name.lower():
                return VectorizableType.Vector3D

        if oop.class_name.lower() in {'marker'}:
            if 'target' in oop.method.name.lower():
                return VectorizableType.Vector3D

        if oop.class_name.lower() in {'ped'}:
            if 'target' in oop.method.name.lower():
                return VectorizableType.Vector3D

        if 'matrix' in oop.method.name.lower():
            return VectorizableType.Matrix

    @staticmethod
    def is_vectorizable_method_return_type(oop: FunctionOOP) -> Optional[VectorizableType]:
        if not oop.method:
            return None

        if not oop.method.name.startswith('get'):
            return None

        if oop.class_name.lower() in {'element', 'player', 'ped', 'mtasaobject', 'vehicle', 'camera', 'marker',
                                      'searchlight'}:
            if 'position' in oop.method.name.lower() \
                    or 'rotation' in oop.method.name.lower() \
                    or 'velocity' in oop.method.name.lower():
                return VectorizableType.Vector3D

        if oop.class_name.lower() in {'mtasaobject'}:
            if 'scale' in oop.method.name.lower():
                return VectorizableType.Vector3D

        if oop.class_name.lower() in {'marker'}:
            if 'target' in oop.method.name.lower():
                return VectorizableType.Vector3D

        if oop.class_name.lower() in {'ped'}:
            if 'target' in oop.method.name.lower():
                return VectorizableType.Vector3D

        if 'matrix' in oop.method.name.lower():
            return VectorizableType.Matrix

    @staticmethod
    def vectorize_field(field: FunctionOOPField, how: VectorizableType) -> None:
        field.types = [
            FunctionType(
                names=[how.value],
                is_optional=False,
            )
        ]

    @staticmethod
    def vectorize_method_args(method: FunctionData, how: VectorizableType) -> None:
        method.signature.arguments.arguments = [
            [FunctionArgument(
                name='vectorized',
                argument_type=FunctionType(
                    names=[how.value],
                    is_optional=False,
                ),
                default_value=None,
            )],
            *method.signature.arguments.arguments[6 if how == VectorizableType.Matrix else 3:]
        ]

    @staticmethod
    def vectorize_method_return_type(method: FunctionData, how: VectorizableType) -> None:
        method.signature.return_types.return_types = [
            FunctionType(
                names=[how.value],
                is_optional=False,
            )
        ]

    def vectorize_oop_if_possible(self, oop: FunctionOOP):
        field_vectorize = self.is_vectorizable_field(oop)
        if field_vectorize:
            self.vectorize_field(oop.field, field_vectorize)

            print(f'    Vectorized field \x1b[34m{oop.class_name}.{oop.field.name}\x1b[0m')

        method_vectorize = self.is_vectorizable_method_args(oop)
        if method_vectorize:
            self.vectorize_method_args(oop.method, method_vectorize)
            print(f'    Vectorized method args \x1b[34m{oop.class_name}.{oop.method.name}\x1b[0m')

        method_vectorize = self.is_vectorizable_method_return_type(oop)
        if method_vectorize:
            self.vectorize_method_return_type(oop.method, method_vectorize)
            print(f'    Vectorized method return types \x1b[34m{oop.class_name}.{oop.method.name}\x1b[0m')

    def apply(self):
        for oop in self.context.oops:
            for side, data in oop:
                data: List[FunctionOOP]

                for oop_inner in data:
                    self.vectorize_oop_if_possible(oop_inner)

        print('Generated vectorized definitions for OOP declarations\u001b[0m')
