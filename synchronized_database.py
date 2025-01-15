import win32event
import win32file
import win32api
from persistent_database import PersistentDatabase


class SynchronizedDatabase(PersistentDatabase):
    def __init__(self, path, mode):
        super().__init__(path)
        self.mode = mode
        self.write_mutex = win32event.CreateMutex(None, False, None)
        self.read_semaphore = win32event.CreateSemaphore(None, 10, 10, None)
        self.read_count_mutex = win32event.CreateMutex(None, False, None)
        self.active_readers = 0

    def acquire_read(self):
        win32event.WaitForSingleObject(self.read_semaphore, win32event.INFINITE)
        win32event.WaitForSingleObject(self.read_count_mutex, win32event.INFINITE)
        self.active_readers += 1
        if self.active_readers == 1:
            win32event.WaitForSingleObject(self.write_mutex, win32event.INFINITE)
        win32event.ReleaseMutex(self.read_count_mutex)

    def release_read(self):
        win32event.WaitForSingleObject(self.read_count_mutex, win32event.INFINITE)
        self.active_readers -= 1
        if self.active_readers == 0:
            win32event.ReleaseMutex(self.write_mutex)
        win32event.ReleaseMutex(self.read_count_mutex)
        win32event.ReleaseSemaphore(self.read_semaphore, 1)

    def acquire_write(self):
        win32event.WaitForSingleObject(self.write_mutex, win32event.INFINITE)

    def release_write(self):
        win32event.ReleaseMutex(self.write_mutex)

    def set_value(self, key, value):
        self.acquire_write()
        try:
            return super().get_value(key)
        finally:
            self.release_write()

    def get_value(self, key):
        self.acquire_read()
        try:
            return super().get_value(key)
        finally:
            self.release_read()

    def delete_value(self, key):
        self.acquire_write()
        try:
            super().delete_value(key)
        finally:
            self.release_write()

    def close_handles(self):
        win32api.CloseHandle(self.write_mutex)
        win32api.CloseHandle(self.read_semaphore)
        win32api.CloseHandle(self.read_count_mutex)
        win32file.CloseHandle(self.file_handle)

    def __del__(self):
        self.close_handles()
