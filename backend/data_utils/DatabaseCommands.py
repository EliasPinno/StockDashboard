import sqlite3
from sqlite3 import Error
import os
from typing import List, Tuple

DB_FILENAME = os.environ.get("DB_FILENAME")
STOCK_TABLE_NAME = os.environ.get("STOCK_TABLE_NAME")
class Database:

    conn: None | sqlite3.Connection = None

    @classmethod
    def getConnection(cls, connectionSrc = DB_FILENAME) -> sqlite3.Connection:
        """
        This method returns a database connection if one exists, or creates a new one
        if it does not already exist.
        """
        #global conn
        if not cls.conn: # We need to create connection
            cls.conn = sqlite3.connect(connectionSrc)
        return cls.conn

    @classmethod
    def closeConnection(cls) -> None:
        """
        This method closes an existing database connection, setting the singleton to none.
        This method does nothing if a connection does not exist.
        """
        if cls.conn: # connection exists, we need to close it
            cls.conn.close()

    @classmethod
    def createDatabase(cls):
        """
        This function creates the table(s) for the database if they do not already exist.
        """
        cls.conn = Database.getConnection()
        cursor = cls.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS {} (
            ticker TEXT CHECK(length(ticker) <= 5),
            date DATE,
            price FLOAT
            PRIMARY KEY (ticker, date)
        )
        '''.format(STOCK_TABLE_NAME))
        # TODO: Think about putting in an is_stored table
        cursor.close()

    @classmethod
    def dropTable(cls):
        """
        This function drops the table, wiping out the local cache if it exists
        """
        cls.conn = Database.getConnection()
        cursor = cls.conn.cursor()
        cursor.execute("DROP TABLE {}".format(STOCK_TABLE_NAME))
        print("Dropped table {}".format(STOCK_TABLE_NAME))
        cursor.close()

    @classmethod
    def getAllDataForTicker(cls,ticker: str):
        """
        Gets all the stored data in the database for a requested ticker
        """
        cls.conn = Database.getConnection()
        cursor = cls.conn.cursor()
        select_query = "SELECT * FROM {} WHERE ticker=?".format(STOCK_TABLE_NAME)
        cursor.execute(select_query, (ticker,))
        result = cursor.fetchall()
        cursor.close()
        return result
    
    @classmethod
    def insertData(cls, data: List[Tuple[str,str,float]]):
        """
        Inserts all the given date formatted in a list of tuples. Tuples should be
        ordered as (ticker, date, price).
        """
        cls.conn = Database.getConnection()
        insert_query = 'INSERT INTO {} (ticker, date, price) VALUES (?,?,?)'.format(STOCK_TABLE_NAME)
        cursor = cls.conn.cursor()
        cursor.executemany(insert_query, data)
        cls.conn.commit()
        cursor.close()

"""
DATABASE = None
def DB():
    if not DATABASE:
        return 
    pass
"""