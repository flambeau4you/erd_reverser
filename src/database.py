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

class Database:
    """
    Database interface
    """
    host = "127.0.0.1"
    user = None
    password = None
    database = None
    port = 3306
    connection = None
            
    def connect(self):
        """
        Connects to database.
        """
        pass
    
    def disconnect(self):
        """
        Disconnects 
        """
        pass
    
    def list_relation_table_names(self):
        """
        Gets all table names with relation information.
        return is ['name which has foreign keys'] = related_name which has primary keys.
        """
        pass
    
    def list_related_table_names(self, filter_name):
        """
        Gets related table names.
        """
        pass
    
    def list_table_names(self):
        """
        Gets all table names
        """
        pass
            
    def list_columns(self, table_name):
        """
        Gets headers.
        """
        pass
