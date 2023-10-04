import requests
import sys
import os

class AlphaVantageAPI:

    def __init__(self, apiKey):
        self.apiKey = apiKey

    def getTickerData(self,ticker):
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&apikey={}'.format(ticker,self.apiKey)
        r = requests.get(url)
        data = r.json()
        print(data["Time Series (Daily)"]["2023-10-03"])

APIInstance = None
def getAlphaVantageAPIInstance() -> AlphaVantageAPI:
    """
    Creates a singleton AlphaVantageAPI object if it does not exist. Returns a AlphaVantageAPI object.
    Must run 'source .env' and have these environment variables for the method to work.
    """
    if not APIInstance:
        APIInstance = AlphaVantageAPI(os.environ.get("API_KEY","demo"))
    return APIInstance

def main(*args):
    avApi = getAlphaVantageAPIInstance()
    avApi.getTickerData("IBM")

if __name__ == "__main__":
    main(*sys.argv)

