from django.contrib import admin
from django.utils.timesince import timesince

from .models import Card, Contact


class ReceivedFilter(admin.SimpleListFilter):
    """Filter postcards by their receive/claim status."""
    title = 'received (claimed)'
    parameter_name = 'received'

    def lookups(self, request, model_admin):
        return (
            ('T', 'yes'),
            ('F', 'no'),
        )

    def queryset(self, request, queryset):
        print(repr(self.value()))
        if self.value() == 'T':
            return queryset.filter(received_at__isnull=False)
        if self.value() == 'F':
            return queryset.filter(received_at__isnull=True)
        return queryset


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = (
        'from_country',
        'from_city',
        'to',
        'sent_at',
        'received_at',
        'delivery_time',

    )
    list_filter = (
        'from_city',
        'to',
        ReceivedFilter,
    )
    ordering = ('-created_at',)

    def delivery_time(self, obj):
        """Calculate the time between sending and claiming the postcard."""
        if not obj.sent_at or not obj.received_at:
            return

        return timesince(obj.sent_at, obj.received_at)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'country',
        'language',
    )

    list_filter = (
        'language',
    )

    ordering = ('name',)
