# Design

## Command Line Parameters

Below is requirement.

1. Host or IP address
1. ID
1. Password
1. Database name

Below is optional.

1. Database system name
1. Port number

## Python File

1. erdr.py: Main script.
1. database.py: Database interface
1. mariadb.py: Handle MariaDB class. It extends database interface.
1. column.py: Column class

## Relation

1. All relation symbols are '}o..o| '.
Left is that table has foreign keys, right is that table has primary keys.