"""
Author: Ido Karadi
Project name: DB API
Description: Part of the DB API program.
This file includes the ThreadChecker class, which includes logic for the tests file.
Date: 15/1/25
"""


from synchronized_database import SynchronizedDatabase
import threading
import time
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


class ThreadChecker:
    def __init__(self, db_path):
        self.db_path = db_path

    def run(self):
        db = SynchronizedDatabase(self.db_path, mode="threads")

        def writer_task():
            db.set_value("key", "value")
            time.sleep(1)
            logging.info("Writer finished writing.")

        def reader_task():
            try:
                db.get_value("key")
            except KeyError:
                pass
            logging.info("Reader finished reading.")

        def delayed_reader_task():
            db.get_value("key")
            time.sleep(2)
            logging.info("Delayed reader finished reading.")

        writer = threading.Thread(target=writer_task)
        reader = threading.Thread(target=reader_task)
        writer.start()
        time.sleep(0.2)
        reader.start()
        writer.join()
        reader.join()

        readers = [threading.Thread(target=reader_task) for _ in range(10)]
        for reader in readers:
            reader.start()
        for reader in readers:
            reader.join()

        delayed_reader = threading.Thread(target=delayed_reader_task)
        writer_waiting = threading.Thread(target=writer_task)
        delayed_reader.start()
        time.sleep(0.2)
        writer_waiting.start()
        delayed_reader.join()
        writer_waiting.join()

        logging.info("ThreadChecker finished.")
