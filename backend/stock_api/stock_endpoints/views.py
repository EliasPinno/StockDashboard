from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
@api_view(["GET"])
def getAllDataForTicker(request, ticker: str):
    return Response({"ticker": ticker})

@api_view(["POST"])
def getDataForSingleDay(request):
    return Response(request)

@api_view(["POST"])
def getDataForDateRange(request):
    return Response({"diff": "ticker"})