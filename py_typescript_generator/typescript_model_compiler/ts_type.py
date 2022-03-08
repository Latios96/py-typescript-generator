from dataclasses import dataclass


@dataclass(frozen=True)
class TsType:
    name: str
    is_optional: bool = False

    def as_optional_type(self):
        # type: ()->TsType
        return TsType(name=self.name, is_optional=True)

    def with_is_optional(self, is_optional):
        # type: (bool)->TsType
        return TsType(name=self.name, is_optional=is_optional)
