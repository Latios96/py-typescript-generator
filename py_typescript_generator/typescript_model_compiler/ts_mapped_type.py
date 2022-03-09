from py_typescript_generator.typescript_model_compiler.ts_type import TsType


class TsMappedType(TsType):
    def __init__(self, wrapped_type: TsType, is_optional: bool = False):
        super(TsMappedType, self).__init__(
            f"{{[index: string]: {wrapped_type.name}}}", is_optional
        )
        self._wrapped_type = wrapped_type

    def as_optional_type(self):
        # type: ()->TsMappedType
        return TsMappedType(wrapped_type=self._wrapped_type, is_optional=True)

    def with_is_optional(self, is_optional):
        # type: (bool)->TsMappedType
        return TsMappedType(wrapped_type=self._wrapped_type, is_optional=is_optional)

    @property
    def wrapped_type(self) -> TsType:
        return self._wrapped_type

    def __str__(self):
        return f"TsMappedType(name='{self.name}', wrapped_type={self.wrapped_type}, is_optional='{self.is_optional}')"

    def __hash__(self):
        return hash((self.name, self.wrapped_type, self.is_optional))

    def __eq__(self, other):
        return (
            other
            and self.name == other.name
            and self.wrapped_type == other.wrapped_type
            and self.is_optional == other.is_optional
        )

    def format_as_type_reference(self):
        return self._format_as_optional(
            f"{{[index: string]: {self.wrapped_type.name}}}"
        )
