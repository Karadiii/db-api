import pickle
from database import Database
import win32file
import pywintypes


class PersistentDatabase(Database):
    def __init__(self, path):
        super().__init__()
        self.file_handle = win32file.CreateFile(
            path,
            win32file.GENERIC_READ | win32file.GENERIC_WRITE,
            0,
            None,
            win32file.OPEN_ALWAYS,
            win32file.FILE_ATTRIBUTE_NORMAL,
            None
        )
        self._load_data()

    def _load_data(self):
        try:
            size = win32file.GetFileSize(self.file_handle)
            if size > 0:
                _, data = win32file.ReadFile(self.file_handle, size)
                self.data = pickle.loads(data)
        except (EOFError, pickle.UnpicklingError):
            self.data = {}

    def save_data(self):
        serialized_data = pickle.dumps(self.data)
        win32file.SetFilePointer(self.file_handle, 0, pywintypes.NULL, win32file.FILE_BEGIN)
        win32file.SetEndOfFile(self.file_handle)
        win32file.WriteFile(self.file_handle, serialized_data)

    def __del__(self):
        win32file.CloseHandle(self.file_handle)
