from dataclasses import dataclass
from ingredient_weight_unit import IngredientWeightUnit


# -1 means NULL
@dataclass
class Ingredient:
    creation_date: str
    update_date: str
    name: str
    energy: int
    protein: float
    carbohydrates: float
    fat: float
    weight_units: list
    license_author: str = 'wger.floss'
    status: str = '2'
    carbohydrates_sugar: float = 0
    fat_saturated: float = 0
    fibres: float = 0
    sodium: float = 0
    language_id: int = 13
    license_id: int = 1
