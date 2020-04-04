from dataclasses import dataclass
from weight_unit import WeightUnit


@dataclass
class IngredientWeightUnit:
    gram: int
    amount: float
    weight_unit: WeightUnit
    ingredient_id: int = -1
    unit_id: int = -1
    id: int = -1
