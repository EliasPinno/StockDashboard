import requests
import sys
import os

class AlphaVantageAPI:

    def __init__(self, apiKey):
        self.apiKey = apiKey

    #TODO: Add exception handling for bad request responses
    def getTickerData(self,ticker: str):
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&apikey={}'.format(ticker,self.apiKey)
        r = requests.get(url)
        data = r.json()
        return data

def getAlphaVantageAPIInstance() -> AlphaVantageAPI:
    """
    Creates an AlphaVantageAPI object if it does not exist. Returns a AlphaVantageAPI object.
    Must run 'source .env' and have these environment variables for the method to work.
    """
    return AlphaVantageAPI(os.environ.get("API_KEY","demo"))

