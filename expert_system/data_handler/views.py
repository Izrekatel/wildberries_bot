from rest_framework import generics

from api.serializers import (RequestPositionSerializer,
                             RequestRateSerializer,
                             RequestStockSerializer)
from data_handler.models import RequestPosition, RequestRate, RequestStock


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
