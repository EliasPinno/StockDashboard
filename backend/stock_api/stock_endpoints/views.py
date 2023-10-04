import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .data_utils.AlphaVantage import getAlphaVantageAPIInstance
from .data_utils.DatabaseCommands import getDBInstance
from typing import List

@api_view(["GET"])
def getAllDataForTicker(request, ticker: str):
    """
    Returns a response with all of the data stored for a given ticker.
    """
    if len(ticker) > 5:
        return Response({"error":"Ticker is too long."}, status=400)
    updateTickerList([ticker])
    db = getDBInstance()
    print("Data is now cached, returning cache.")
    result = db.getAllDataForTicker(ticker)
    db.closeConnection()
    return Response({"result": result})

@api_view(["POST"])
def getDataForSingleDay(request):
    """
        Returns all of the data for the given tickers for the given day.
    """
    try:
        request_data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return Response({"error": "Invalid JSON data"}, status=400)
    tickers = request_data.get("tickers", [])
    date = request_data.get("date", "")
    updateTickerList(tickers)
    db = getDBInstance()
    result = db.getDataInDateRange(tickers,date,date)
    db.closeConnection()
    return Response(result)

@api_view(["POST"])
def getDataForDateRange(request):
    """
    Returns all of the data for the given tickers for the given date range.
    """
    try:
        request_data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return Response({"error": "Invalid JSON data"}, status=400)
    tickers = request_data.get("tickers", [])
    aboveDate = request_data.get("aboveDate", "")
    belowDate = request_data.get("belowDate", "")
    updateTickerList(tickers)
    db = getDBInstance()
    result = db.getDataInDateRange(tickers,aboveDate,belowDate)
    db.closeConnection()
    return Response(result)

# TODO: Turn this into a proper endpoint, and have the other views just send an HTTP request
#@api_view(["POST"])
def updateTickerList(tickers: List[str]):
    db = getDBInstance()
    api = getAlphaVantageAPIInstance()
    cachedTicker = db.getMostRecentDateForTickers(tickers)
    for ticker in tickers:
        apiResponse = api.getTickerData(ticker)
        dataToCache = apiResponse["Time Series (Daily)"]
        dbFormOfData = []
        if ticker not in cachedTicker:
            print("{} not in db: cache from scratch.".format(ticker))
            for date in dataToCache.keys():
                dbFormOfData.append((ticker, date, dataToCache[date]["4. close"]))
            db.insertData(dbFormOfData)
        elif cachedTicker[ticker] != apiResponse["Meta Data"]["3. Last Refreshed"]:
            for date in dataToCache.keys():
                if date > cachedTicker[ticker]:
                    dbFormOfData.append((ticker, date, dataToCache[date]["4. close"]))
                else:
                    break
            pass
    db.closeConnection()
    return