import sqlite3
from sqlite3 import Error

DB_FILENAME = "PROJECT_DB"
STOCK_TABLE_NAME = "stock_prices"

class Database:
    conn: None | sqlite3.Connection = None

    @staticmethod
    def getConnection():
        """
        This method returns a database connection if one exists, or creates a new one
        if it does not already exist.
        """
        global conn
        if not conn: # We need to create connection
            conn = sqlite3.connect(DB_FILENAME)
        return conn

    @staticmethod
    def closeConnection():
        """
        This method closes an existing database connection, setting the singleton to none.
        """
        global conn
        if conn: # connection exists, we need to close it
            conn.close()

    @staticmethod
    def createDatabase():
        """
        This function creates the table(s) for the database if they do not already exist
        """
        conn = sqlite3.connect(DB_FILENAME)
