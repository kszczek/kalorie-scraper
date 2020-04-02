import sqlite3


class Database:
    def __init__(self, path):
        self.db = sqlite3.connect(path)

    def insert_ingredient(self, ingredient):
        query = ('INSERT INTO nutrition_ingredient (license_author, status, creation_date, update_date, '
                 'name, energy, protein, carbohydrates, carbohydrates_sugar, fat, fat_saturated, fibres, '
                 'sodium, language_id, license_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)')
        parameters = (ingredient.license_author, ingredient.status, ingredient.creation_date, ingredient.update_date,
                      ingredient.name, ingredient.energy, ingredient.protein, ingredient.carbohydrates,
                      ingredient.carbohydrates_sugar, ingredient.fat, ingredient.fat_saturated, ingredient.fibres,
                      ingredient.sodium, ingredient.language_id, ingredient.license_id)
        cursor = self.db.cursor()
        cursor.execute(query, parameters)
        self.db.commit()

    def close(self):
        self.db.commit()
        self.db.close()
