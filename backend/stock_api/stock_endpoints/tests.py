from unittest.mock import patch
from django.test import TestCase
#import stock_api.stock_endpoints as se
from .data_utils.DatabaseCommands import Database
from .views import getAllDataForTicker
from django.http import HttpRequest

# Create your tests here.
class StockEndpointsTests(TestCase):

    db = None
    def setUp(self):
        self.db = Database("test_DB", "test_table")
        self.db.createDatabase()

    def tearDown(self):
        self.db.dropTable()
        self.db.closeConnection()
    
    @patch('stock_endpoints.views.updateTickerList')
    def test_get_all_data_for_ticker(self, mock_update_ticker_list):
        # insert some values into our db to see
        self.db.insertData([("ABC","2023-10-04",10.0)])
        # prevent API call from happening
        mock_update_ticker_list.return_value = None  # Replace with desired return value
        request = HttpRequest()
        request.method = "GET"
        result = getAllDataForTicker(request, ticker="ABC")

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data, {"result": {"ticker":"ABC", "prices":{"2023-10-04":10.0}}})

"""
class DatabaseTests(TestCase):

    db = None

    @classmethod
    def setUpClass(cls):
        cls.db = Database("test_DB", "test_table")
        cls.db.dropTable()
        cls.db.createDatabase()
        cls.db.closeConnection()

    def setUp(self):
        self.db.createDatabase()

    def tearDown(self):
        self.db.dropTable()
        self.db.closeConnection()

    def test_createTable(self):
        print("Running test_createTable")

    def test_insertData(self):
        print("Running test_insertData")

    def test_getAllDataForTicker(self):
        print("Running test_getAllDataForTicker")
    
    def test_getMostRecentDateForTickers(self):
        print("Running test_getMostRecentDateForTickers")
"""