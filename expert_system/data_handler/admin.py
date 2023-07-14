from django.contrib import admin

from .models import (
    TelegramUser,
    RequestPosition,
    RequestStock,
    RequestRate
)


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id", "add_time",)
    list_display_links = ("user_id",)
    search_fields = ("id", "user_id", "add_time",)
    list_filter = ("user_id", "add_time",)


@admin.register(RequestPosition)
class RequestPositionAdmin(admin.ModelAdmin):
    list_display = ("id", "add_time", "articul", "text",)
    search_fields = ("id", "add_time", "articul", "text",)
    list_filter = ("add_time", "articul", "text",)


@admin.register(RequestRate)
class RequestRateAdmin(admin.ModelAdmin):
    list_display = ("id", "add_time", "warehouse_id",)
    search_fields = ("id", "add_time", "warehouse_id",)
    list_filter = ("add_time", "warehouse_id",)


@admin.register(RequestStock)
class RequestStockAdmin(admin.ModelAdmin):
    list_display = ("id", "add_time", "articul",)
    search_fields = ("id", "add_time", "articul",)
    list_filter = ("add_time", "articul",)
