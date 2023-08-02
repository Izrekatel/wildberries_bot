from rest_framework import generics, viewsets

from api.serializers import (
    FrequencyRequestPositionSerializer,
    RequestPositionSerializer,
    RequestRateSerializer,
    RequestStockSerializer,
    TelegramUserSerializer,
)
from data_handler.models import (
    FrequencyRequestPosition,
    RequestPosition,
    RequestRate,
    RequestStock,
    TelegramUser,
)


class RequestPositionViewSet(viewsets.ModelViewSet):
    """Добавление, редактирование, удаление Position в БД."""

    serializer_class = RequestPositionSerializer
    queryset = RequestPosition.objects.all()
    lookup_field = "telegram_user"


class RequestStockViewSet(generics.CreateAPIView):
    """Добавление Stock в БД."""

    serializer_class = RequestStockSerializer
    queryset = RequestStock.objects.all()


class RequestRateViewSet(generics.CreateAPIView):
    """Добавление Rate в БД."""

    serializer_class = RequestRateSerializer
    queryset = RequestRate.objects.all()


class FrequencyRequestPositionViewSet(viewsets.ModelViewSet):
    """Добавление Rate в БД."""

    serializer_class = FrequencyRequestPositionSerializer
    queryset = FrequencyRequestPosition.objects.all()
    lookup_field = "frequency"


class TelegramUserViewSet(viewsets.ModelViewSet):
    """Добавление, редактирование, удаление TelegramUser в БД."""

    serializer_class = TelegramUserSerializer
    queryset = TelegramUser.objects.all()
    lookup_field = "user_id"
