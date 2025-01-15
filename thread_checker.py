import threading
import time
from synchronized_database import SynchronizedDatabase


class ThreadChecker:
    def __init__(self, path):
        self.db = SynchronizedDatabase(path, mode='threads')

    def writer(self):
        self.db.set_value('key', 'value')
        time.sleep(1)

    def reader(self):
        value = self.db.get_value('key')
        time.sleep(1)

    def delayed_reader(self):
        time.sleep(2)
        value = self.db.get_value('key')

    def run(self):
        threads = [threading.Thread(target=self.writer)]
        for _ in range(10):
            threads.append(threading.Thread(target=self.reader))
        threads.append(threading.Thread(target=self.delayed_reader))

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
