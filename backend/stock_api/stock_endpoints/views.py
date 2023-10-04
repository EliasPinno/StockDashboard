from rest_framework.decorators import api_view
from rest_framework.response import Response
from .data_utils.AlphaVantage import getAlphaVantageAPIInstance
from .data_utils.DatabaseCommands import getDBInstance

@api_view(["GET"])
def getAllDataForTicker(request, ticker: str):
    """
    Returns a response with all of the data stored for a given ticker.
    """
    if len(ticker) > 5:
        return Response({"result":"error"})
    db = getDBInstance()
    #db.dropTable()
    #db.createDatabase()
    cachedTicker = db.getMostRecentDateForTickers([ticker])
    api = getAlphaVantageAPIInstance()
    apiResponse = api.getTickerData(ticker)
    if ticker not in cachedTicker:
        print("Ticker not in db: cache from scratch.")
        dataToCache = apiResponse["Time Series (Daily)"]
        dbFormOfData = []
        for date in dataToCache.keys():
            print(date)
            dbFormOfData.append((ticker, date, dataToCache[date]["4. close"]))
        print(dbFormOfData)
        db.insertData(dbFormOfData)
    elif cachedTicker[ticker] != apiResponse["Meta Data"]["3. Last Refreshed"]:
        print("Ticker in db but not updated: compute diff")
        pass
    print("Data is now cached, returning cache.")
    return Response({"result":db.getAllDataForTicker(ticker)})

@api_view(["POST"])
def getDataForSingleDay(request):
    """
    Returns all of the data for the given tickers for the given day.
    """
    return Response(request)

@api_view(["POST"])
def getDataForDateRange(request):
    """
    Returns all of the data for the given tickers for the given date range.
    """
    return Response({"diff": "ticker"})