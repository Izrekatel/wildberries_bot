from data_handler.views import (
    RequestPositionViewSet,
    RequestRateViewSet,
    RequestStockViewSet,
    TelegramUserViewSet,
)
from django.urls import path

app_name = "api"

urlpatterns = [
    path(
        "request_position/",
        RequestPositionViewSet.as_view(),
        name="new_request_position",
    ),
    path(
        "request_stock/",
        RequestStockViewSet.as_view(),
        name="new_request_stock",
    ),
    path(
        "request_rate/", RequestRateViewSet.as_view(), name="new_request_rate"
    ),
    path(
        "telegram_user/",
        TelegramUserViewSet.as_view(),
        name="new_telegram_user",
    ),
]
