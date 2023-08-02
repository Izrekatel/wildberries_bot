from django.urls import include, path
from rest_framework.routers import DefaultRouter

from data_handler.views import (
    FrequencyRequestPositionViewSet,
    RequestPositionViewSet,
    RequestRateViewSet,
    RequestStockViewSet,
    TelegramUserViewSet,
)

app_name = "api"
router = DefaultRouter()

router.register("telegram_user", TelegramUserViewSet, "telegram_users")
router.register(
    "request_position", RequestPositionViewSet, "request_positions"
)
router.register("frequency", FrequencyRequestPositionViewSet, "frequencies")


urlpatterns = [
    # path(
    #    "request_position/",
    #    RequestPositionViewSet.as_view(),
    #    name="new_request_position",
    # ),
    path(
        "request_stock/",
        RequestStockViewSet.as_view(),
        name="new_request_stock",
    ),
    path(
        "request_rate/", RequestRateViewSet.as_view(), name="new_request_rate"
    ),
    path("", include(router.urls)),
]
