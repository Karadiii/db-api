"""
Author: Ido Karadi
Project name: DB API
Description: Part of the DB API program.
This file includes the ProcessChecker class, which includes logic for the tests file.
Date: 15/1/25
"""


from synchronized_database import SynchronizedDatabase
import multiprocessing
import time
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


def writer_task(db_path, lock):
    with lock:
        db = SynchronizedDatabase(db_path, mode="processes")
        db.set_value("key", "value")
        time.sleep(1)
        logging.info("Writer finished writing.")


def reader_task(db_path, lock):
    with lock:
        db = SynchronizedDatabase(db_path, mode="processes")
        try:
            db.get_value("key")
        except KeyError:
            pass
        logging.info("Reader finished reading.")


def delayed_reader_task(db_path, lock):
    with lock:
        db = SynchronizedDatabase(db_path, mode="processes")
        db.get_value("key")
        time.sleep(2)
        logging.info("Delayed reader finished reading.")


class ProcessChecker:
    def __init__(self, db_path):
        self.db_path = db_path

    def run(self):
        lock = multiprocessing.Lock()
        writer = multiprocessing.Process(target=writer_task, args=(self.db_path, lock))
        reader = multiprocessing.Process(target=reader_task, args=(self.db_path, lock))
        writer.start()
        time.sleep(0.2)
        reader.start()
        writer.join()
        reader.join()

        readers = [multiprocessing.Process(target=reader_task, args=(self.db_path, lock)) for _ in range(10)]
        for reader in readers:
            reader.start()
        for reader in readers:
            reader.join()

        delayed_reader = multiprocessing.Process(target=delayed_reader_task, args=(self.db_path, lock))
        writer_waiting = multiprocessing.Process(target=writer_task, args=(self.db_path, lock))
        delayed_reader.start()
        time.sleep(0.2)
        writer_waiting.start()
        delayed_reader.join()
        writer_waiting.join()

        logging.info("ProcessChecker finished.")
