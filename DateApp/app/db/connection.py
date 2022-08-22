from heavyai import connect
from sqlalchemy import create_engine
import os
import sqlite3
from .load_periodo import load_periodo

postgres_connection_string="postgresql://user_longrungrowth:YjkqSNQ_CG6M25TKf@postgresql11.db.huma-num.fr/longrungrowth"
omnisci_connection_string="mapd://LongRunGrowth:w5BJSkf8RUzTb7Aj@omnisci.db.huma-num.fr:6278/LongRunGrowth?protocol=https"


db_created = False
path = os.path.dirname(os.path.realpath(__file__))

#sqlite
engine=f"sqlite:///{path}/../DateCleaning.db"
def create_db():
    with open(path + "/../create_sqlite_tables.sql", 'r') as sql_file:
        sql_script = sql_file.read()

    conn = sqlite3.connect(path + "/../DateCleaning.db")
    cursor = conn.cursor()
    cursor.executescript(sql_script)
    conn.commit()

    global db_created
    db_created = True
    print("created sqlite for test")

def get_engine():
    if not db_created:
        create_db()
        load_periodo(engine)
    return engine

def get_postgre_connection():
    # return postgres_connection_string
    return get_engine()

def get_omnisci_connection():
    # return connect(omnisci_connection_string)
    return get_engine()

def get_omnisci_con_string():
    return omnisci_connection_string

if __name__ == "__main__":
    print("started")
    create_engine(postgres_connection_string)
    print("conected")