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

    def insert_ingredient(self, ingredient):
        logging.info('Inserting ingredient {}'.format(ingredient.name))
        query = ('INSERT INTO nutrition_ingredient (license_author, status, creation_date, update_date, '
                 'name, energy, protein, carbohydrates, carbohydrates_sugar, fat, fat_saturated, fibres, '
                 'sodium, language_id, license_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)')
        parameters = (ingredient.license_author, ingredient.status, ingredient.creation_date, ingredient.update_date,
                      ingredient.name, ingredient.energy, ingredient.protein, ingredient.carbohydrates,
                      ingredient.carbohydrates_sugar, ingredient.fat, ingredient.fat_saturated, ingredient.fibres,
                      ingredient.sodium, ingredient.language_id, ingredient.license_id)
        cursor = self.db.cursor()
        cursor.execute(query, parameters)
        ingredient.id = cursor.lastrowid
        for weight_unit in ingredient.weight_units:
            weight_unit.ingredient_id = ingredient.id
        self.db.commit()
        cursor.close()
        if len(ingredient.weight_units) > 0:
            self.insert_ingredient_weight_units(ingredient.weight_units)

    def insert_weight_units(self, weight_units):
        logging.info('Inserting {} weight units'.format(len(weight_units)))
        query = 'INSERT INTO nutrition_weightunit (name, language_id) VALUES (?, ?)'
        cursor = self.db.cursor()
        for weight_unit in weight_units:
            parameters = (weight_unit.name, weight_unit.language_id)
            cursor.execute(query, parameters)
            weight_unit.id = cursor.lastrowid
            self.weight_units.append(weight_unit)
        self.db.commit()
        cursor.close()

    def insert_ingredient_weight_units(self, ingredient_weight_units):
        logging.info('Inserting {} ingredient weight units'.format(len(ingredient_weight_units)))
        units_to_insert = []
        for unit in ingredient_weight_units:
            found = False
            for weight_unit in self.weight_units:
                if weight_unit.name == unit.weight_unit.name:
                    found = True
                    break
            if not found:
                units_to_insert.append(unit.weight_unit)
        if len(units_to_insert) > 0:
            self.insert_weight_units(units_to_insert)
        parameters = []
        for unit in ingredient_weight_units:
            if unit.unit_id == -1:
                for weight_unit in self.weight_units:
                    if weight_unit.name == unit.weight_unit.name:
                        unit.unit_id = weight_unit.id
                        break
            parameters.append((unit.gram, unit.amount, unit.ingredient_id, unit.unit_id))
        query = 'INSERT INTO nutrition_ingredientweightunit (gram, amount, ingredient_id, unit_id) VALUES (?, ?, ?, ?)'
        cursor = self.db.cursor()
        cursor.executemany(query, parameters)
        self.db.commit()
        cursor.close()

    def close(self):
        self.db.commit()
        self.db.close()
