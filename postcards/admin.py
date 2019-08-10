from django.contrib import admin

from .models import Card, Contact


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    pass


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    pass
