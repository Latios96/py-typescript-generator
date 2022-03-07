from dataclasses import dataclass


@dataclass(frozen=True)
class TsObjectType:
    name: str
