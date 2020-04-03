from bs4 import BeautifulSoup
from utils import simple_get
from ingredient import Ingredient
from datetime import datetime
import logging


class Scraper:
    BASE_URL = 'http://kalkulatorkalorii.net/tabela-kalorii/{}'

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
                float(tds[4].text.replace(',', '.'))
            ))
        return ingredients

    def get_page(self, page):
        return simple_get(self.BASE_URL.format(page))