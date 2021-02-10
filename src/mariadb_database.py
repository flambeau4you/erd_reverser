# Copyright 2020 Jung Bong-Hwa
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import mariadb
import sys
from database import Database
from column import Column
from pickle import TRUE

class MariadbDatabase(Database):
    """
    MariaDB implementation
    """
            
    def connect(self):
        try:
            self.connection = mariadb.connect(
                host = self.host,
                user = self.user,
                password = self.password,
                database = self.database,
                port = self.port
            )
        except mariadb.Error as e:
            print(f"Error connecting to database: {e}")
            sys.exit(1)
        return self.connection
    
    def disconnect(self):
        self.connection.close()
    
    def list_relation_table_names(self):
        cursor = self.connection.cursor()
        sql = """
            select TABLE_NAME, REFERENCED_TABLE_NAME 
            from INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
            where REFERENCED_TABLE_SCHEMA = ?
            """
        cursor.execute(sql, (self.database,))    
        rows = cursor.fetchall()
        table_names = {}
        old_name = ""
        for table_name, referenced_table_name in rows:
            if table_name != old_name:
                table_names[table_name] = []
            try:
                table_names[table_name].index(referenced_table_name)
            except ValueError:
                table_names[table_name].append(referenced_table_name)
            old_name = table_name
            
        return table_names

    def list_related_table_names(self, filter_name):
        table_names = self.list_relation_table_names()
        filter_names = {}
        for table_name in table_names:
                
            if table_name == filter_name:
                filter_names[table_name] = table_names[table_name]
            else:
                for ref_name in table_names[table_name]:
                    if ref_name == filter_name:                        
                        filter_names[table_name] = []
                        filter_names[table_name].append(ref_name)
                        break
                
        return filter_names
    
    def list_table_names(self):
        cursor = self.connection.cursor()
        sql = """
            select TABLE_NAME
            from INFORMATION_SCHEMA.TABLES 
            where TABLE_SCHEMA = ? 
            order by TABLE_NAME
            """
        cursor.execute(sql, (self.database,))    
        rows = cursor.fetchall()
        table_names = []
        for table_name in rows:
            table_names.append(table_name)
            
        return table_names

    def list_columns(self, table_name):
        cursor = self.connection.cursor()
        sql = """
            select COLUMN_NAME, COLUMN_TYPE, COLUMN_KEY, IS_NULLABLE 
            from INFORMATION_SCHEMA.COLUMNS 
            where TABLE_SCHEMA = ? and TABLE_NAME = ?
            """
        cursor.execute(sql, (self.database, table_name,))    
        rows = cursor.fetchall()
        columns = []
        for column_name, column_type, column_key, is_nullable in rows:
            column = Column()
            column.name = column_name
            column.type = column_type
            column.is_primary = column_key == 'PRI'
            column.is_nullable = is_nullable == 'YES'
            columns.append(column)

        # Foreign keys
        cursor = self.connection.cursor()
        sql = """
            select COLUMN_NAME 
            from INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
            where REFERENCED_TABLE_SCHEMA = ? and TABLE_NAME = ?
            """
        cursor.execute(sql, (self.database, table_name,))    
        rows = cursor.fetchall()
        for column_name in rows:
            for column in columns:
                if column.name == column_name[0]:
                    column.is_foreign = True
                    break
                
        return columns

