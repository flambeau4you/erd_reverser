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
from mariadb_database import MariadbDatabase 

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

def reverse(db, filter_name=None):    
    # Relations
    if filter_name == None:
        relations = db.list_relation_table_names()
    else:
        relations = db.list_related_table_names(filter_name)

    if filter_name == None:
        table_names = db.list_table_names()
    else:
        table_names = []
        for table_name in relations:
            table_names.append(table_name)
        
    texts = []
    for table_name in table_names:
        texts.append(f"entity { table_name } {{")
        columns = db.list_columns(table_name)
        for column in columns:
            if column.primary:
                prefix = "*"
            elif column.foreign:
                prefix = "+"
            else:
                prefix = ""
            texts.append(f"{ prefix }`{ column.name }`")
        texts.append("}}")
        
    for table_name in relations:
        texts.append(f"{ table_name }||..||{ relations[table_name] }")
        
    return texts;    
    
def write_file(file_name, texts):
    fo = codecs.open(file_name, encoding='utf-8', mode='w')
    fo.write("@startuml\n")
    for text in texts:
        fo.write(text + "\n")
    fo.write("@enduml\n")
    fo.close()
    
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
    
    if db_system == DB_MARIADB:
        db = MariadbDatabase()
    else:
        print(f"{ db_system } is not supported yet.")
        sys.exit(1)
        
    db.host = args.parameters[0]
    db.user = args.parameters[1]
    db.password = args.parameters[2]
    db.database = db_name
    db.port = db_port
         
    # Connect to MariaDB Platform
    db.connect()
    
    texts = reverse(db, args.table)
    
    db.disconnect()
    
    if len(texts) == 0:
        print("Result is empty")
        sys.exit(1)
        
    write_file(file_name, texts)