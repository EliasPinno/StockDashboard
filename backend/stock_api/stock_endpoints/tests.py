from django.test import TestCase
from data_utils.DatabaseCommands import Database

# Create your tests here.
class StockEndpointsTests(TestCase):
    
    def test(self):
        self.assertEqual(True,True)
        print("test ran")

class DatabaseTests(TestCase):

    db = None

    @classmethod
    def setUpClass(cls):
        cls.db = Database("test_db", "test_table")

    @classmethod
    def tearDownClass(cls):
        cls.db.closeConnection()
        cls.db = None

    def setUp(self):
        self.db.createDatabase()

    def tearDown(self):
        self.db.dropTable()

    def test_createTable(self):
        print("Running test_createTable")

    def test_insertData(self):
        print("Running test_insertData")

    def test_getAllDataForTicker(self):
        print("Running test_getAllDataForTicker")
    
    def test_getMostRecentDateForTickers(self):
        print("Running test_getMostRecentDateForTickers")