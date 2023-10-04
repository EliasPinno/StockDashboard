import requests
import sys
import os

class AlphaVantageAPI:

    @staticmethod
    def getTickerData(ticker,apiKey):
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&apikey={}'.format(ticker,apiKey)
        r = requests.get(url)
        data = r.json()
        print(data["Time Series (Daily)"]["2023-10-03"])


def main(*args):
    # remember to source .env for running this.
    # source .env
    apiKey = os.environ.get("API_KEY","demo")
    AlphaVantageAPI.getTickerData("IBM",apiKey)

if __name__ == "__main__":
    main(*sys.argv)

