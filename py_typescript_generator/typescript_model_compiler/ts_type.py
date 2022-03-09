from dataclasses import dataclass
from enum import Enum


class TsTypeKind(Enum):
    INTERFACE = "INTERFACE"
    ARRAY = "ARRAY"


@dataclass(frozen=True)
class TsType:
    name: str
    is_optional: bool = False
    kind: TsTypeKind = TsTypeKind.INTERFACE

    @staticmethod
    def array(name: str, is_optional: bool = False):
        return TsType(name=name, is_optional=is_optional, kind=TsTypeKind.ARRAY)

    def as_optional_type(self):
        # type: ()->TsType
        return TsType(name=self.name, is_optional=True, kind=self.kind)

    def with_is_optional(self, is_optional):
        # type: (bool)->TsType
        return TsType(name=self.name, is_optional=is_optional, kind=self.kind)
