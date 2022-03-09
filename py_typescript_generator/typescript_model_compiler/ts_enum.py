from dataclasses import dataclass
from typing import Union, FrozenSet


@dataclass(frozen=True)
class TsEnum:
    name: str
    values: FrozenSet[Union[int, str]]
