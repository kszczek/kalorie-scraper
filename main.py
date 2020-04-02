from queue import Queue
from threading import Thread, Lock
from database import Database
import logging
import sys

parser_done: bool = False
lock = Lock()
queue = Queue()


def scraper_worker():
    while True:
        print('working')
        break
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
        if queue.not_empty:
            db.insert_ingredient(queue.get(False))


if __name__ == '__main__':
    if not len(sys.argv) == 1:
        exit(1)
    logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.INFO, datefmt='%H:%M:%S')
    parser_thread = Thread(scraper_worker)
    database_thread = Thread(database_worker, sys.argv[0])
    logging.info('Starting parser thread')
    parser_thread.start()
    logging.info('Staring database thread')
    database_thread.start()
    parser_thread.join()
    database_thread.join()
    logging.info('Both threads finished')

