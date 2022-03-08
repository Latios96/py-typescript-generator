from dataclasses import dataclass


@dataclass(frozen=True)
class TsType:
    name: str
    is_optional: bool = False
