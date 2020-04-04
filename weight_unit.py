from dataclasses import dataclass


@dataclass
class WeightUnit:
    name: str
    id: int = -1
    language_id: int = 13
