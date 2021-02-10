# Developer Guide

## Python

If it is Ubuntu, install MariaDB Connector fistly.

```bash
curl -sS https://downloads.mariadb.com/MariaDB/mariadb_repo_setup | sudo bash
sudo apt install mariadb3
sudo apt install mariadb-dev
```

Install additional modules.

```bash
pip3 install mariadb
```

## Eclipse

Use Eclipse with PyDev plugin for developing.

## PlantUML

Download the jar file at https://plantuml.com/.

Install graphviz tool.

```bash
sudo apt install graphviz
```

Run as below.

```bash
java -jar plantuml.jar -tpng FILE.txt
```

