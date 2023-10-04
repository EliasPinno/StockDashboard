from django.urls import path

from .views import (
    getAllDataForTicker,
    getDataForDateRange
)

urlpatterns = [
    path("getAllData/<str:ticker>", getAllDataForTicker),
    path("getDataForSingleDay", getAllDataForTicker),
    path("getDataForDateRange", getDataForDateRange),
]