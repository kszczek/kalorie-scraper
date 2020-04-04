from queue import Queue
from threading import Thread, Lock
from database import Database
from scraper import Scraper
import logging
import sys

parser_done: bool = False
lock = Lock()
queue = Queue()


def scraper_worker():
    scraper = Scraper()
    page = 1
    while True:
        logging.info('Parsing page {}'.format(page))
        ingredients = scraper.get_ingredients(page)
        if len(ingredients) == 0:
            break
        for ingredient in ingredients:
            queue.put(ingredient)
        page += 1
    lock.acquire()
    global parser_done
    parser_done = True
    lock.release()


def database_worker(path):
    db = Database(path)
    global parser_done
    while True:
        lock.acquire()
        if parser_done and queue.empty():
            break
        lock.release()
        if not queue.empty():
            db.insert_ingredient(queue.get(False))
    db.close()


if __name__ == '__main__':
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.INFO, datefmt='%H:%M:%S', handlers=[handler])
    if not len(sys.argv) == 2:
        logging.info('No correct arguments supplied')
        exit(1)
    parser_thread = Thread(target=scraper_worker)
    database_thread = Thread(target=database_worker, args=[sys.argv[1]])
    logging.info('Starting parser thread')
    parser_thread.start()
    logging.info('Staring database thread')
    database_thread.start()
    parser_thread.join()
    database_thread.join()
    logging.info('Both threads finished')

