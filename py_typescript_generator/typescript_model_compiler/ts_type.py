class TsType:
    def __init__(self, name: str, is_optional: bool = False):
        self._name = name
        self._is_optional = is_optional

    @property
    def name(self) -> str:
        return self._name

    @property
    def is_optional(self) -> bool:
        return self._is_optional

    def as_optional_type(self):
        # type: ()->TsType
        return TsType(name=self.name, is_optional=True)

    def with_is_optional(self, is_optional):
        # type: (bool)->TsType
        return TsType(name=self.name, is_optional=is_optional)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"TsType(name='{self.name}', is_optional='{self.is_optional}')"

    def __hash__(self):
        return hash((self.name, self.is_optional))

    def __eq__(self, other):
        return (
            other and self.name == other.name and self.is_optional == other.is_optional
        )

    def format_as_type_reference(self):
        return self.name
