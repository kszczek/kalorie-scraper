import sqlite3
import logging
from weight_unit import WeightUnit


class Database:
    weight_units = []

    def __init__(self, path):
        self.db = sqlite3.connect(path)
        cursor = self.db.cursor()
        for row in cursor.execute('SELECT id, name, language_id FROM nutrition_weightunit'):
            self.weight_units.append(WeightUnit(
                row[1],
                row[0],
                row[2]
            ))
        cursor.close()

    def get_last_ingredient_id(self):
        cursor = self.db.cursor()
        cursor.execute('SELECT id FROM nutrition_ingredient ORDER BY id DESC LIMIT 1')
        result = cursor.fetchone()
        if result == None:
            result = 0
        else:
            result = result[0]
        cursor.close()
        return result

    def insert_ingredient(self, ingredient):
        logging.info('Inserting ingredient {}'.format(ingredient.name))
        query = ('INSERT INTO nutrition_ingredient (id, license_author, status, creation_date, update_date, '
                 'name, energy, protein, carbohydrates, carbohydrates_sugar, fat, fat_saturated, fibres, '
                 'sodium, language_id, license_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)')
        parameters = (ingredient.id, ingredient.license_author, ingredient.status, ingredient.creation_date,
                      ingredient.update_date, ingredient.name, ingredient.energy, ingredient.protein,
                      ingredient.carbohydrates, ingredient.carbohydrates_sugar, ingredient.fat, ingredient.fat_saturated,
                      ingredient.fibres, ingredient.sodium, ingredient.language_id, ingredient.license_id)
        cursor = self.db.cursor()
        cursor.execute(query, parameters)
        self.db.commit()
        cursor.close()

    def insert_weight_unit(self, weight_unit):
        logging.info('Inserting weight unit {}'.format(weight_unit.name))
        query = 'INSERT INTO nutrition_weightunit (name, language_id) VALUES (?, ?)'
        cursor = self.db.cursor()
        cursor.execute(query, (weight_unit.name, weight_unit.language_id))
        weight_unit.id = cursor.lastrowid
        self.weight_units.append(weight_unit)
        self.db.commit()
        cursor.close()
        return weight_unit.id

    def insert_ingredient_weight_unit(self, ingredient_weight_unit):
        found = False
        for weight_unit in self.weight_units:
            if weight_unit.name == ingredient_weight_unit.weight_unit.name:
                found = True
                ingredient_weight_unit.unit_id = weight_unit.id
                break
        if not found:
            ingredient_weight_unit.unit_id = self.insert_weight_unit(ingredient_weight_unit.weight_unit)
        query = 'INSERT INTO nutrition_ingredientweightunit (gram, amount, ingredient_id, unit_id) VALUES (?, ?, ?, ?)'
        cursor = self.db.cursor()
        cursor.execute(query, (ingredient_weight_unit.gram, ingredient_weight_unit.amount,
                                ingredient_weight_unit.ingredient_id, ingredient_weight_unit.unit_id))
        self.db.commit()
        cursor.close()

    def close(self):
        self.db.commit()
        self.db.close()
