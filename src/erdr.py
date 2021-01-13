#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

import argparse
import json
import re
import sys
import codecs

DB_MARIADB = 'mariadb_database'

# Defines arguments.
parser = argparse.ArgumentParser(description='ERD Reverser')
parser.add_argument("-s", "--system", 
                    help="DBMS name. Default: mariadb_database")
parser.add_argument("-p", "--port", 
                    help="Port number.")
parser.add_argument("-t", "--table", 
                    help="Filter by the name.")
parser.add_argument('parameters', metavar='parameter', nargs='*',
                    help="host ID password DB file")

if __name__ == '__main__':
    args = parser.parse_args()
    
    # Validates arguments.
    if len(args.parameters) < 5:
        parser.print_help(sys.stderr)
        sys.exit(1)
        
    db_system = DB_MARIADB
    
    if args.system:
        db_system = args.system
         
    if args.port:
        db_port = args.port
    elif db_system == DB_MARIADB:
        db_port = 3306
    
    db_name = args.parameters[3]
    file_name = args.parameters[4]
         
    # Connect to MariaDB Platform
    try:
        conn = mariadb.connect(
            host = args.parameters[0],
            user = args.parameters[1],
            password = args.parameters[2],
            database = db_name,
            port = db_port
        )
    except mariadb.Error as e:
        print(f"Error connecting to database: {e}")
        sys.exit(1)
    
    # Gets cursor.
    cur = conn.cursor()
    
    if db_system == DB_MARIADB:
        cur.execute(
            "select TABLE_NAME as table_name, TABLE_TYPE as table_type from INFORMATION_SCHEMA.TABLES where TABLE_SCHEMA = ? order by TABLE_NAME", (db_name,))
    
    table_result = cur.fetchall()
    count = 0
    fo = codecs.open(file_name, encoding='utf-8', mode='w')
    for table_name, table_type in table_result:
        fo.write(f"[`{ table_name }`]\n")
        
        # Columns
        if db_system == DB_MARIADB:
            cur.execute(
                "select COLUMN_NAME, COLUMN_TYPE, COLUMN_KEY from INFORMATION_SCHEMA.COLUMNS where TABLE_SCHEMA = ? and TABLE_NAME = ?", (db_name, table_name,))
            column_result = cur.fetchall()
            for column_name, column_type, column_key in column_result:
                if column_key == "PRI":
                    prefix = "*"
                elif column_key == "MUL":
                    prefix = "+"
                else:
                    prefix = ""
            
                fo.write(f"{ prefix }`{ column_name }`\n")
                
        fo.write("\n")
            
        count += 1
        
    if count == 0:
        print("Result is empty.")
        fo.close()
        conn.close()
        sys.exit(1)
    
    # Relations    
    if db_system == DB_MARIADB:
        cur.execute("select TABLE_NAME, REFERENCED_TABLE_NAME from INFORMATION_SCHEMA.KEY_COLUMN_USAGE where REFERENCED_TABLE_SCHEMA = ?", (db_name,))    
    referenced_result = cur.fetchall()
    for table_name, referenced_table_name in referenced_result:
        fo.write(f"`{ table_name }` -- `{ referenced_table_name }`\n")
    
    fo.close()
    conn.close()
    
