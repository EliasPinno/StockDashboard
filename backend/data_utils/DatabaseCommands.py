import sqlite3
from sqlite3 import Error

class Database:
    DB_FILENAME = "PROJECT_DB"
    STOCK_TABLE_NAME = "stock_prices"
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
        '''.format(Database.STOCK_TABLE_NAME))
        # TODO: Think about putting in an is_stored table
        cursor.close()

    @classmethod
    def dropTable(cls):
        """
        This function drops the table, wiping out the local cache if it exists
        """
        cls.conn = Database.getConnection()
        cursor = cls.conn.cursor()
        cursor.execute("DROP TABLE {}".format(Database.STOCK_TABLE_NAME))
        print("Dropped table {}".format(Database.STOCK_TABLE_NAME))
        cursor.close()
