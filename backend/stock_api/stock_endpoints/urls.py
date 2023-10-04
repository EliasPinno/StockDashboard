from django.urls import path

from .views import (
    getAllDataForTicker
)

urlpatterns = [
    path("getAllData/<str:ticker>", getAllDataForTicker),
]