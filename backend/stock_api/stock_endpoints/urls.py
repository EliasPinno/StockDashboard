from django.urls import path

from .views import (
    getAllDataForTicker,
    getDataForDateRange,
    getDataForSingleDay,
)

urlpatterns = [
    path("getAllData/<str:ticker>", getAllDataForTicker),
    path("getDataForSingleDay", getDataForSingleDay),
    path("getDataForDateRange", getDataForDateRange),
]