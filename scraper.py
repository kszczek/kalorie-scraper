from bs4 import BeautifulSoup
from utils import simple_get
from ingredient import Ingredient
from ingredient_weight_unit import IngredientWeightUnit
from weight_unit import WeightUnit
from datetime import datetime
from time import sleep
import re


class Scraper:
    BASE_URL = 'http://kalkulatorkalorii.net'
    PAGE_URL = BASE_URL + '/tabela-kalorii/{}'

    def get_ingredients(self, page):
        soup = BeautifulSoup(self.get_page(page), 'html.parser')
        ingredients = []
        tbody = soup.find('tbody')
        for tr in tbody.find_all('tr'):
            tds = tr.find_all('td')
            date = datetime.now().date()
            ingredients.append(Ingredient(
                date,
                date,
                tds[0].text.strip(),
                int(tds[1].text),
                float(tds[2].text.replace(',', '.')),
                float(tds[3].text.replace(',', '.')),
                float(tds[4].text.replace(',', '.')),
                self.BASE_URL + tds[0].find('a')['href']
            ))
        return ingredients

    def get_ingredient_weight_units(self, ingredient):
        response = simple_get(ingredient.details_url)
        if response == None:
            return None
        soup = BeautifulSoup(response, 'html.parser')
        uls = soup.find_all('ul', class_='suggestions')
        if not len(uls) == 3:
            return None
        root = uls[1]
        ingredient_weight_units = []
        for li in root.find_all('li'):
            weight_unit = IngredientWeightUnit(
                int(re.sub('[^0-9]', '', li.find('i').text)),
                1,
                WeightUnit(li.find('strong').text.lower())
            )
            weight_unit.ingredient_id = ingredient.id
            ingredient_weight_units.append(weight_unit)
        return ingredient_weight_units

    def get_page(self, page):
        response = simple_get(self.PAGE_URL.format(page))
        while response == None:
            sleep(3)
            simple_get(self.PAGE_URL.format(page))
        return response
