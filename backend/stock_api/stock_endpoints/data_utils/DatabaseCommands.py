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
                       price FLOAT, 
                       PRIMARY KEY (ticker, date))
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
        select_query = "SELECT date, price FROM {} WHERE ticker=? ORDER BY date DESC".format(self.STOCK_TABLE_NAME)
        cursor.execute(select_query, (ticker,))
        result = cursor.fetchall()
        cursor.close()
        resultMap = {"ticker": ticker, "prices": {}}
        for row in result:
            resultMap["prices"][row[0]] = row[1]
        return resultMap
    
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
        select_query = "SELECT ticker, MAX(date) AS max_date FROM {} WHERE ticker IN ({}) GROUP BY ticker".format(self.STOCK_TABLE_NAME,','.join(['?'] * len(tickers)))
        print(select_query)
        cursor.execute(select_query, tickers)
        result = cursor.fetchall()
        cursor.close()
        resultMap = {}
        for row in result:
            resultMap[row[0]] = row[1]
        return resultMap
    
    def getDataInDateRange(self, tickers: List[str], aboveDate, belowDate):
        conn = self.getConnection()
        cursor = conn.cursor()
        select_query = "SELECT ticker, date, price FROM {} WHERE ticker IN ({}) AND date >= ? AND date <= ? ORDER BY ticker, date DESC".format(self.STOCK_TABLE_NAME, ','.join(['?'] * len(tickers)))
        cursor.execute(select_query, tickers + [aboveDate, belowDate])
        result = cursor.fetchall()
        cursor.close()
        resultList = []
        for ticker, date, price in result:
            resultList.append({"ticker":ticker, "date":date, "price":price})
        return resultList

def getDBInstance() -> Database:
    """
    Creates a Database object if it does not exist. Returns a database object.
    Must run 'source .env' and have these environment variables set for the method to work
    """
    DB_FILENAME = os.environ.get("DB_FILENAME")
    STOCK_TABLE_NAME = os.environ.get("STOCK_TABLE_NAME")
        
    return Database(DB_FILENAME, STOCK_TABLE_NAME)

if __name__ == "__main__":
    db = getDBInstance()
    db.createDatabase()
    db.getMostRecentDateForTickers(["IBM"])


