from api.serializers import (
    CitySerializer,
    FrequencyRequestPositionSerializer,
    RequestPositionSerializer,
    RequestRateSerializer,
    RequestStockSerializer,
    TelegramUserSerializer,
    WarehouseSerializer,
)
from data_handler.models import (
    City,
    FrequencyRequestPosition,
    RequestPosition,
    RequestRate,
    RequestStock,
    TelegramUser,
    Warehouse,
)
from rest_framework import viewsets
from rest_framework.response import Response


class FrequencyViewSet(viewsets.ModelViewSet):
    """Получение списка FrequencyRequestPosition из БД."""

    http_method_names = ("get",)
    serializer_class = FrequencyRequestPositionSerializer
    queryset = FrequencyRequestPosition.objects.all()
    lookup_field = "frequency"


class RequestPositionViewSet(viewsets.ModelViewSet):
    """Добавление, редактирование, удаление, получение списка Position в БД."""

    serializer_class = RequestPositionSerializer
    lookup_field = "user_id"

    def retrieve(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        if self.action in ("retrieve",):
            return RequestPosition.objects.filter(
                user_id=self.kwargs.get("user_id")
            )
        return RequestPosition.objects.all()


class RequestStockViewSet(viewsets.ModelViewSet):
    """Добавление Stock в БД."""

    serializer_class = RequestStockSerializer
    queryset = RequestStock.objects.all()
    http_method_names = ("post",)


class RequestRateViewSet(viewsets.ModelViewSet):
    """Добавление Rate в БД."""

    serializer_class = RequestRateSerializer
    queryset = RequestRate.objects.all()
    http_method_names = ("post",)


class TelegramUserViewSet(viewsets.ModelViewSet):
    """Добавление, редактирование, удаление TelegramUser в БД."""

    serializer_class = TelegramUserSerializer
    queryset = TelegramUser.objects.all()
    lookup_field = "user_id"


class CityViewSet(viewsets.ModelViewSet):
    """CRUD для City в БД."""

    serializer_class = CitySerializer
    queryset = City.objects.all()


class WarehouseViewSet(viewsets.ModelViewSet):
    """CRUD для Warehouse в БД."""

    serializer_class = WarehouseSerializer
    queryset = Warehouse.objects.all()
