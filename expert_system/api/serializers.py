from data_handler.models import (
    City,
    FrequencyRequestPosition,
    RequestPosition,
    RequestRate,
    RequestStock,
    TelegramUser,
    Warehouse,
)
from rest_framework import serializers


class TelegramUserSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = TelegramUser
        fields = (
            "user_id",
            "e_mail",
        )
        search_field = "user_id"


class FrequencyRequestPositionSerializer(serializers.ModelSerializer):
    frequency = serializers.IntegerField()

    class Meta:
        model = FrequencyRequestPosition
        fields = ("frequency",)


class RequestPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestPosition
        fields = (
            "articul",
            "text",
            "user_id",
            "frequency",
            "last_request",
        )
        search_field = "user_id"

    def validate(self, attrs):
        # надо вынести в отдельный файл.
        if self.context["request"].method != "POST":
            return attrs
        if RequestPosition.objects.filter(**attrs).exists():
            raise serializers.ValidationError("This object already exists")
        return attrs


class RequestStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestStock
        fields = (
            "articul",
            "user_id",
        )

    def validate(self, attrs):
        if self.context["request"].method != "POST":
            return attrs
        if RequestStock.objects.filter(**attrs).exists():
            raise serializers.ValidationError("This object already exists")
        return attrs


class RequestRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestRate
        fields = (
            "warehouse_id",
            "user_id",
        )

    def validate(self, attrs):
        if self.context["request"].method != "POST":
            return attrs
        if RequestRate.objects.filter(**attrs).exists():
            raise serializers.ValidationError("This object already exists")
        return attrs


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = (
            "city",
            "location",
        )

    def validate(self, attrs):
        if self.context["request"].method != "POST":
            return attrs
        if RequestStock.objects.filter(**attrs).exists():
            raise serializers.ValidationError("This object already exists")
        return attrs


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = (
            "number",
            "name",
        )

    def validate(self, attrs):
        if self.context["request"].method != "POST":
            return attrs
        if RequestStock.objects.filter(**attrs).exists():
            raise serializers.ValidationError("This object already exists")
        return attrs
