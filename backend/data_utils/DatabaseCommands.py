import sqlite3
from sqlite3 import Error

class Database:
    DB_FILENAME = "PROJECT_DB"
    STOCK_TABLE_NAME = "stock_prices"
    #IS_STORED_TABLE_NAME = "is_stored"
    conn: None | sqlite3.Connection = None

    @staticmethod
    def getConnection(connectionSrc = DB_FILENAME) -> sqlite3.Connection:
        """
        This method returns a database connection if one exists, or creates a new one
        if it does not already exist.
        """
        global conn
        if not conn: # We need to create connection
            conn = sqlite3.connect(connectionSrc)
        return conn

    @staticmethod
    def closeConnection() -> None:
        """
        This method closes an existing database connection, setting the singleton to none.
        This method does nothing if a connection does not exist.
        """
        global conn
        if conn: # connection exists, we need to close it
            conn.close()

    @staticmethod
    def createDatabase():
        """
        This function creates the table(s) for the database if they do not already exist.
        """
        conn = Database.getConnection()
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS {} (
            ticker TEXT CHECK(length(ticker) <= 5),
            date DATE,
            price FLOAT
            PRIMARY KEY (ticker, date)
        )
        '''.format(Database.STOCK_TABLE_NAME))
        # TODO: Think about putting in an is_stored table
        cursor.close()

    @staticmethod
    def dropTable():
        """
        This function drops the table, wiping out the local cache if it exists
        """
        conn = Database.getConnection()
        cursor = conn.cursor()
        cursor.execute("DROP TABLE {}".format(Database.STOCK_TABLE_NAME))
        print("Dropped table {}".format(Database.STOCK_TABLE_NAME))
        cursor.close()
