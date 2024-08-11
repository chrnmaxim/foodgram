from django.contrib import admin
from subscriptions.models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Определяет отображение подписок в панели администратора."""

    list_display = ["author", "user"]
