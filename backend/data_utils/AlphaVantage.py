import requests
import sys
import os

class AlphaVantageAPI:

    @classmethod
    def getTickerData(ticker,apiKey):
        print(cls.apiKey)
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&apikey={}'.format(ticker,cls.apiKey)
        r = requests.get(url)
        data = r.json()
        print(data)


def main(*args):
    # remember to source .env for running this.
    # source .env
    apiKey = os.environ.get("API_KEY","demo")
    AlphaVantageAPI.getTickerData("IBM",apiKey)
    pass

if __name__ == "__main__":
    main(*sys.argv)

