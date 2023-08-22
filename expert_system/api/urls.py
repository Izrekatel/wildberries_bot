from data_handler.views import (
    CityViewSet,
    FrequencyViewSet,
    RequestPositionViewSet,
    RequestRateViewSet,
    RequestStockViewSet,
    TelegramUserViewSet,
    WarehouseViewSet,
)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = "api"
router = DefaultRouter()

router.register("telegram_user", TelegramUserViewSet, "telegram_users")
router.register(
    "request_position", RequestPositionViewSet, "request_positions"
)
router.register("request_stock", RequestStockViewSet, "stock_requests")
router.register("request_rate", RequestRateViewSet, "rate_requests")
router.register("frequency", FrequencyViewSet, "frequency_requests")
router.register("city", CityViewSet, "city_requests")
router.register("warehouse", WarehouseViewSet, "warehouse_requests")

urlpatterns = [
    path("", include(router.urls)),
]
