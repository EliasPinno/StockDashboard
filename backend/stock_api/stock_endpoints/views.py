from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(["GET"])
def getAllDataForTicker(request, ticker: str):
    """
    Returns a response with all of the data stored for a given ticker.
    """
    return Response({"ticker": ticker})

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