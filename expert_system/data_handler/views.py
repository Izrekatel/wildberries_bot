from api.serializers import (
    RequestPositionSerializer,
    RequestRateSerializer,
    RequestStockSerializer,
    TelegramUserSerializer,
)
from data_handler.models import (
    RequestPosition,
    RequestRate,
    RequestStock,
    TelegramUser,
)
from rest_framework import generics


class RequestPositionViewSet(generics.CreateAPIView):
    """Добавление Position в БД."""

    serializer_class = RequestPositionSerializer
    queryset = RequestPosition.objects.all()


class RequestStockViewSet(generics.CreateAPIView):
    """Добавление Stock в БД."""

    serializer_class = RequestStockSerializer
    queryset = RequestStock.objects.all()


class RequestRateViewSet(generics.CreateAPIView):
    """Добавление Rate в БД."""

    serializer_class = RequestRateSerializer
    queryset = RequestRate.objects.all()


class TelegramUserViewSet(generics.CreateAPIView):
    """Добавление TelegramUser в БД."""

    serializer_class = TelegramUserSerializer
    queryset = TelegramUser.objects.all()
