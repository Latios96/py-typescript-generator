from py_typescript_generator.typescript_model_compiler.ts_type import TsType


class TsArray(TsType):
    def __init__(self, wrapped_type: TsType, is_optional: bool = False):
        super(TsArray, self).__init__(f"{wrapped_type.name}[]", is_optional)
        self._wrapped_type = wrapped_type

    def as_optional_type(self):
        # type: ()->TsArray
        return TsArray(wrapped_type=self._wrapped_type, is_optional=True)

    def as_non_optional_type(self):
        # type: ()->TsArray
        return TsArray(wrapped_type=self._wrapped_type, is_optional=False)

    def with_is_optional(self, is_optional):
        # type: (bool)->TsArray
        return TsArray(wrapped_type=self._wrapped_type, is_optional=is_optional)

    @property
    def wrapped_type(self) -> TsType:
        return self._wrapped_type

    def __str__(self):
        return f"TsArray(name='{self.name}', wrapped_type={self.wrapped_type}, is_optional='{self.is_optional}')"

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
        formatted_wrapped_type = f"{self.wrapped_type.format_as_type_reference()}"
        return self._format_as_optional(f"{formatted_wrapped_type}[]")
