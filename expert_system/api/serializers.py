# import datetime as dt

from rest_framework import serializers

from data_handler.models import (
    FrequencyRequestPosition,
    RequestPosition,
    RequestRate,
    RequestStock,
    TelegramUser,
)


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
    # telegram_user = serializers.IntegerField()
    frequency = serializers.ReadOnlyField(source="frequency.frequency")

    # def get_frequency(self, obj):
    #    print(self.context)
    #    return 3

    # def get_telegram_user(self, obj):
    #    print(self.context)
    #    return 3

    class Meta:
        model = RequestPosition
        depth = 1
        fields = (
            "articul",
            "text",
            "telegram_user",
            "frequency",
            "last_request",
        )

    # def validate(self, attrs):
    #    if self.context["request"].method != "POST":
    #        return attrs
    #    if RequestPosition.objects.filter(**attrs).exists():
    #        raise serializers.ValidationError("This object already exists")
    #    return attrs


class RequestStockSerializer(serializers.ModelSerializer):
    articul = serializers.IntegerField()
    telegram_user = TelegramUserSerializer(many=False)

    class Meta:
        model = RequestStock
        fields = (
            "articul",
            "telegram_user",
        )

    def validate(self, attrs):
        if self.context["request"].method != "POST":
            return attrs
        if RequestStock.objects.filter(**attrs).exists():
            raise serializers.ValidationError("This object already exists")
        return attrs


class RequestRateSerializer(serializers.ModelSerializer):
    warehouse_id = serializers.IntegerField()
    telegram_user = TelegramUserSerializer(many=False)

    class Meta:
        model = RequestRate
        fields = (
            "warehouse_id",
            "telegram_user",
        )

    def validate(self, attrs):
        if self.context["request"].method != "POST":
            return attrs
        if RequestRate.objects.filter(**attrs).exists():
            raise serializers.ValidationError("This object already exists")
        return attrs
