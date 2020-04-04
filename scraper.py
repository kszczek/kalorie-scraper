from bs4 import BeautifulSoup
from utils import simple_get
from ingredient import Ingredient
from ingredient_weight_unit import IngredientWeightUnit
from weight_unit import WeightUnit
from datetime import datetime
import re
import logging


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
                self.get_ingredient_weight_units(self.BASE_URL + tds[0].find('a')['href'])
            ))
            logging.info('Parsed ingredient {}'.format(tds[0].text.strip()))
        return ingredients

    def get_ingredient_weight_units(self, url):
        response = simple_get(url)
        soup = BeautifulSoup(response, 'html.parser')
        root = soup.find_all('ul', class_='suggestions')[1]
        ingredient_weight_units = []
        for li in root.find_all('li'):
            weight_unit = IngredientWeightUnit(
                int(re.sub('[^0-9]', '', li.find('i').text)),
                1,
                WeightUnit(li.find('strong').text.lower())
            )
            ingredient_weight_units.append(weight_unit)
        return ingredient_weight_units

    def get_page(self, page):
        return simple_get(self.PAGE_URL.format(page))
