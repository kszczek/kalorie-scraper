from queue import Queue, Empty
from threading import Thread, Lock
from database import Database
from scraper import Scraper
import logging
import sys

ingredient_parser_done: bool = False
units_parser_done: bool = False
lock = Lock()
ingredient_queue = Queue()
ingredient_units_queue = Queue()
units_queue = Queue()


def ingredient_worker():
    scraper = Scraper()
    page = 1
    while True:
        ingredients = scraper.get_ingredients(page)
        if len(ingredients) == 0:
            break
        for ingredient in ingredients:
            ingredient_queue.put(ingredient)
            ingredient_units_queue.put(ingredient)
        page += 1
    lock.acquire()
    global ingredient_parser_done
    ingredient_parser_done = True
    lock.release()

def ingredient_units_worker():
    scraper = Scraper()
    while True:
        lock.acquire()
        if ingredient_parser_done and ingredient_units_queue.empty():
            break
        lock.release()
        units = scraper.get_ingredient_weight_units(ingredient_units_queue.get())
        if units == None:
            continue
        for unit in units:
            units_queue.put(unit)
    lock.acquire()
    global units_parser_done
    units_parser_done = True
    lock.release()

def database_worker(path):
    db = Database(path)
    id = db.get_last_ingredient_id() + 1
    global ingredient_parser_done
    global units_parser_done
    while True:
        lock.acquire()
        if ingredient_parser_done and units_parser_done and ingredient_queue.empty() and units_queue.empty():
            break
        lock.release()
        if not ingredient_queue.empty():
            ingredient = ingredient_queue.get(False)
            ingredient.id = id
            id += 1
            db.insert_ingredient(ingredient)
        if not units_queue.empty():
            db.insert_ingredient_weight_unit(units_queue.get(False))
    db.close()


if __name__ == '__main__':
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.INFO, datefmt='%H:%M:%S', handlers=[handler])
    if not len(sys.argv) == 2:
        logging.info('No correct arguments supplied')
        exit(1)
    ingredient_thread = Thread(target=ingredient_worker)
    units_thread = Thread(target=ingredient_units_worker)
    database_thread = Thread(target=database_worker, args=[sys.argv[1]])
    logging.info('Starting ingredient parser thread')
    ingredient_thread.start()
    logging.info('Starting units parser thread')
    units_thread.start()
    logging.info('Staring database thread')
    database_thread.start()
    ingredient_thread.join()
    units_thread.join()
    database_thread.join()
    logging.info('All threads finished')

