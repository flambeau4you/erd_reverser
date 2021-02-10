import unittest
from unittest.mock import MagicMock
import erdr
from database import Database
from column import Column

class TestErdr(unittest.TestCase):
    
    def test_reverse_db_texts(self):
        def list_table_names():
            table_names = ['t1']
            return table_names
        
        def list_columns(table_name): 
            columns = []        
            col = Column()
            col.name = 'c1'
            col.type = 'varchar(10)'
            col.is_primary = True
            col.is_foreign = False
            col.is_nullable = False
            columns.append(col)

            col = Column()
            col.name = 'c2'
            col.type = 'varchar(10)'
            col.is_primary = False
            col.is_foreign = True
            col.is_nullable = True
            columns.append(col)

            return columns
        
        def list_relation_table_names():
            table_names = {'t1': ['r1', 'r2']}
            return table_names

        def list_related_table_names(filter_name):
            table_names = {filter_name: ['r1', 'r2']}
            return table_names
            
        database = MagicMock()
        database.list_table_names = list_table_names
        database.list_columns = list_columns
        database.list_relation_table_names = list_relation_table_names
        database.list_related_table_names = list_related_table_names
        
        texts = erdr.reverse(database)
        self.assertEqual(texts[0], 'entity t1 {')
        self.assertEqual(texts[1], '  *c1 : varchar(10)')
        self.assertEqual(texts[2], '  --')
        self.assertEqual(texts[3], '  c2 : varchar(10) <<FK>>')
        self.assertEqual(texts[4], '}')
        self.assertEqual(texts[5], 't1 ||..|| r1')
        self.assertEqual(texts[6], 't1 ||..|| r2')

        texts = erdr.reverse(database, 't1')
        self.assertEqual(texts[0], 'entity t1 {')

if __name__ == '__main__':
    unittest.main()