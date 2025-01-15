import multiprocessing
import time
from synchronized_database import SynchronizedDatabase


class ProcessChecker:
    def __init__(self, path):
        self.path = path

    def writer(self):
        db = SynchronizedDatabase(self.path, mode='processes')
        db.set_value('key', 'value')
        time.sleep(1)

    def reader(self):
        db = SynchronizedDatabase(self.path, mode='processes')
        value = db.get_value('key')
        time.sleep(1)

    def delayed_reader(self):
        time.sleep(2)
        db = SynchronizedDatabase(self.path, mode='processes')
        value = db.get_value('key')

    def run(self):
        processes = [multiprocessing.Process(target=self.writer)]
        for _ in range(10):
            processes.append(multiprocessing.Process(target=self.reader))
        processes.append(multiprocessing.Process(target=self.delayed_reader))

        for process in processes:
            process.start()
        for process in processes:
            process.join()
