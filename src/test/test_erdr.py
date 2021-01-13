import unittest
from unittest.mock import MagicMock
import erdr
from database import Database

class TestErdr(unittest.TestCase):
    def test_reverse_db_file(self):
        database = Database()
        table_names = ['a', 'b', 'c']
        database.list_table_names = MagicMock(return_value=table_names)
        erdr.reverse(database)

if __name__ == '__main__':
    unittest.main()