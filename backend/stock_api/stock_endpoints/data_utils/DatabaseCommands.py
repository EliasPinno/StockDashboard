import sqlite3
from sqlite3 import Error
import os
from typing import List, Tuple

class Database:

    def __init__(self, DB_FILENAME: str, STOCK_TABLE_NAME: str):
        self.conn: None | sqlite3.Connection = None
        self.DB_FILENAME: str = DB_FILENAME
        self.STOCK_TABLE_NAME: str = STOCK_TABLE_NAME

    def getConnection(self) -> sqlite3.Connection:
        """
        Returns a database connection if one exists, or creates a new one
        if it does not already exist.
        """
        #global conn
        if not self.conn: # We need to create connection
            self.conn = sqlite3.connect(self.DB_FILENAME)
        return self.conn

    def closeConnection(self) -> None:
        """
        Closes an existing database connection, setting the connection to None.
        This method does nothing if a connection does not exist.
        """
        if self.conn: # connection exists, we need to close it
            self.conn.close()
            self.conn = None

    def createDatabase(self):
        """
        Creates the table(s) for the database if they do not already exist.
        """
        conn = self.getConnection()
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS {} (
            ticker TEXT CHECK(length(ticker) <= 5),
            date DATE,
            price FLOAT
            PRIMARY KEY (ticker, date)
        )
        '''.format(self.STOCK_TABLE_NAME))
        # TODO: Think about putting in an is_stored table
        cursor.close()

    def dropTable(self):
        """
        This function drops the table, wiping out the local cache if it exists
        """
        conn = self.getConnection()
        cursor = conn.cursor()
        cursor.execute("DROP TABLE {}".format(self.STOCK_TABLE_NAME))
        print("Dropped table {}".format(self.STOCK_TABLE_NAME))
        cursor.close()

    def getAllDataForTicker(self,ticker: str):
        """
        Gets all the stored data in the database for a requested ticker
        """
        conn = self.getConnection()
        cursor = conn.cursor()
        select_query = "SELECT * FROM {} WHERE ticker=?".format(self.STOCK_TABLE_NAME)
        cursor.execute(select_query, (ticker,))
        result = cursor.fetchall()
        cursor.close()
        return result
    
    def insertData(self, data: List[Tuple[str,str,float]]):
        """
        Inserts all the given date formatted in a list of tuples. Tuples should be
        ordered as (ticker, date, price).
        """
        conn = self.getConnection()
        insert_query = 'INSERT INTO {} (ticker, date, price) VALUES (?,?,?)'.format(self.STOCK_TABLE_NAME)
        cursor = conn.cursor()
        cursor.executemany(insert_query, data)
        conn.commit()
        cursor.close()

    def getMostRecentDateForTickers(self, tickers: List[str]):
        conn = self.getConnection()
        cursor = conn.cursor()
        select_query = "SELECT MAX(date) AS max_date FROM {} WHERE ticker = ({}) GROUP BY ticker".format(self.STOCK_TABLE_NAME,','.join(['?'] * len(tickers)))
        cursor.execute(select_query, tickers)
        result = cursor.fetchall()
        cursor.close()
        return result

DBInstance = None
def getDBInstance() -> Database:
    """
    Creates a singleton Database object if it does not exist. Returns a database object.
    Must run 'source .env' and have these environment variables set for the method to work
    """
    if not DBInstance:
        DB_FILENAME = os.environ.get("DB_FILENAME")
        STOCK_TABLE_NAME = os.environ.get("STOCK_TABLE_NAME")
        DBInstance = Database(DB_FILENAME, STOCK_TABLE_NAME)
    return DBInstance