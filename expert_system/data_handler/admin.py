from django.contrib import admin

from .models import (
    FrequencyRequestPosition,
    RequestPosition,
    RequestRate,
    RequestStock,
    TelegramUser,
)


@admin.register(FrequencyRequestPosition)
class FrequencyRequestPositionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "frequency",
    )
    list_display_links = ("frequency",)
    search_fields = (
        "id",
        "frequency",
    )
    list_filter = ("frequency",)


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user_id",
        "e_mail",
        "add_time",
    )
    list_display_links = (
        "user_id",
        "e_mail",
    )
    search_fields = (
        "id",
        "user_id",
        "e_mail",
        "add_time",
    )
    list_filter = (
        "user_id",
        "e_mail",
        "add_time",
    )


@admin.register(RequestPosition)
class RequestPositionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "add_time",
        "telegram_user",
        "articul",
        "text",
        "frequency",
        "last_request",
    )
    search_fields = (
        "id",
        "add_time",
        "telegram_user",
        "articul",
        "text",
        "frequency",
        "last_request",
    )
    list_filter = (
        "add_time",
        "telegram_user",
        "articul",
        "text",
        "frequency",
        "last_request",
    )


@admin.register(RequestRate)
class RequestRateAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "add_time",
        "telegram_user",
        "warehouse_id",
    )
    search_fields = (
        "id",
        "add_time",
        "telegram_user",
        "warehouse_id",
    )
    list_filter = (
        "add_time",
        "telegram_user",
        "warehouse_id",
    )


@admin.register(RequestStock)
class RequestStockAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "add_time",
        "telegram_user",
        "articul",
    )
    search_fields = (
        "id",
        "add_time",
        "telegram_user",
        "articul",
    )
    list_filter = (
        "add_time",
        "telegram_user",
        "articul",
    )
