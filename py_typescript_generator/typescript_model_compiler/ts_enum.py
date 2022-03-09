from dataclasses import dataclass
from typing import Union, FrozenSet


@dataclass(frozen=True)
class TsEnumValue:
    name: str
    value: Union[int, str]


@dataclass(frozen=True)
class TsEnum:
    name: str
    values: FrozenSet[TsEnumValue]
