from data_handler.models import (
    RequestPosition,
    RequestRate,
    RequestStock,
    TelegramUser,
)
from rest_framework import serializers


class RequestPositionSerializer(serializers.ModelSerializer):
    articul = serializers.IntegerField()
    text = serializers.CharField()

    class Meta:
        model = RequestPosition
        fields = ("articul", "text")

    def validate(self, attrs):
        if self.context["request"].method != "POST":
            return attrs
        if RequestPosition.objects.filter(**attrs).exists():
            raise serializers.ValidationError("This object already exists")
        return attrs


class RequestStockSerializer(serializers.ModelSerializer):
    articul = serializers.IntegerField()

    class Meta:
        model = RequestStock
        fields = ("articul",)

    def validate(self, attrs):
        if self.context["request"].method != "POST":
            return attrs
        if RequestStock.objects.filter(**attrs).exists():
            raise serializers.ValidationError("This object already exists")
        return attrs


class RequestRateSerializer(serializers.ModelSerializer):
    warehouse_id = serializers.IntegerField()

    class Meta:
        model = RequestRate
        fields = ("warehouse_id",)

    def validate(self, attrs):
        if self.context["request"].method != "POST":
            return attrs
        if RequestRate.objects.filter(**attrs).exists():
            raise serializers.ValidationError("This object already exists")
        return attrs


class TelegramUserSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = TelegramUser
        fields = ("user_id",)

    def validate(self, attrs):
        if self.context["request"].method != "POST":
            return attrs
        if TelegramUser.objects.filter(**attrs).exists():
            raise serializers.ValidationError("This object already exists")
        return attrs
