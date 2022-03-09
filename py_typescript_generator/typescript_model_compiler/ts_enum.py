from dataclasses import dataclass
from typing import Union, Tuple


@dataclass(frozen=True)
class TsEnumValue:
    name: str
    value: Union[int, str]

    def format_value(self) -> str:
        if isinstance(self.value, str):
            return f'"{self.value}"'
        return f"{self.value}"


@dataclass(frozen=True)
class TsEnum:
    name: str
    values: Tuple[TsEnumValue, ...]
