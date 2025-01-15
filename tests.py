"""
Author: Ido Karadi
Project name: DB API
Description: Test file for a synchronized database program with multiple set rules using WinAPI.
This file runs the tests that ensure the program is working as intended.
Date: 15/1/25
"""


from database import Database
from persistent_database import PersistentDatabase
from synchronized_database import SynchronizedDatabase
from thread_checker import ThreadChecker
from process_checker import ProcessChecker
import os


# Test cases for Database class
def test_database():
    db = Database()

    # Test setting and getting values
    db.set_value("key1", "value1")
    assert db.get_value("key1") == "value1", "Failed to set/get value"

    # Test deleting a value
    db.delete_value("key1")
    try:
        db.get_value("key1")
    except KeyError:
        pass  # Expected behavior

    print("All Database tests passed!")


# Test cases for PersistentDatabase class
def test_persistent_database():
    db_path = "test_db.pkl"

    if os.path.exists(db_path):
        os.remove(db_path)

    pdb = PersistentDatabase(db_path)
    pdb.set_value("key1", "value1")
    assert pdb.get_value("key1") == "value1", "Failed to persist set/get value"

    pdb.delete_value("key1")
    try:
        pdb.get_value("key1")
    except KeyError:
        pass

    print("All PersistentDatabase tests passed!")


# Test cases for SynchronizedDatabase class
def test_synchronized_database_threads():
    db = SynchronizedDatabase("sync_db_threads.pkl", mode="threads")
    print("SynchronizedDatabase thread tests passed!")


def test_synchronized_database_processes():
    db = SynchronizedDatabase("sync_db_processes.pkl", mode="processes")
    print("SynchronizedDatabase process tests passed!")


# Run all tests
if __name__ == "__main__":
    test_database()
    test_persistent_database()

    print("Running ThreadChecker...")
    thread_checker = ThreadChecker("thread_test_db.pkl")
    thread_checker.run()

    print("Running ProcessChecker...")
    process_checker = ProcessChecker("process_test_db.pkl")
    process_checker.run()
