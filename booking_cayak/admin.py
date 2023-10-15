from sys import path
from django.contrib import admin
from .models import BoatType, Boat, BoatStatus, Booking, Price
from .views import statistics_view


# admin.site.register(BoatType)
# admin.site.register(Boat)
# admin.site.register(BoatStatus)
# admin.site.register(Booking)
# admin.site.register(Price)
# @admin.register(Price)
# class PriceAdmin(admin.ModelAdmin):
# list_display = ('boat', 'duration', 'price_per_hour')
# list_editable = ('price_per_hour',)


class StatisticsAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('statistics/', self.admin_site.admin_view(statistics_view), name='statistics'),
        ]
        return custom_urls + urls


@admin.register(BoatType)
class BoatTypeAdmin(admin.ModelAdmin):
    list_display = ['type_name', 'quantity']
    search_fields = ['type_name']


@admin.register(Boat)
class BoatAdmin(admin.ModelAdmin):
    list_display = ['boat_type', 'boat_index', 'status']
    list_filter = ['status']
    search_fields = ['boat_type__type_name']


@admin.register(BoatStatus)
class BoatStatusAdmin(admin.ModelAdmin):
    list_display = ['boat', 'start_time', 'end_time', 'status']
    list_filter = ['status']
    search_fields = ['boat__boat_type__type_name']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'boat_status', 'start_time', 'duration', 'boat_type', 'discount', 'is_first_time_booking',
                    'special_conditions', 'rental_price', 'calculate_total_price')
    list_filter = ('boat_status', 'boat_type', 'discount', 'is_first_time_booking')
    search_fields = ('boat_status', 'boat_type__type_name', 'discount', 'special_conditions')
    ordering = ('start_time', 'duration', 'boat_type')



@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        capacities = BoatType.objects.values_list('quantity', flat=True).distinct()
        return queryset.filter(capacity__in=capacities)

    @staticmethod
    def get_field_name(capacity):
        if capacity == 1:
            return 'Ціна за годину (1 особа)'
        return f'Ціна за годину ({capacity} осіб)'

    def get_list_display(self, request):
        capacities = BoatType.objects.values_list('quantity', flat=True).distinct()
        fields = ['duration'] + [f'get_price_for_capacity_{capacity}' for capacity in capacities]
        return fields

    @staticmethod
    def get_price_for_capacity(obj, capacity):
        try:
            field_name = f'capacity_{capacity}'
            field_label = getattr(obj, f'capacity_{capacity}_label')
            field_value = getattr(obj, field_name)
            return f'{field_label}: {field_value}'
        except AttributeError:
            return '-'

    def get_fieldsets(self, request, obj=None):
        capacities = BoatType.objects.values_list('quantity', flat=True).distinct()
        fieldsets = [(None, {'fields': ['duration', 'capacity']})]
        for capacity in capacities:
            field_name = f'capacity_{capacity}'
            field_label = self.get_field_name(capacity)
            fieldsets.append((field_label, {'fields': [field_name, f'{field_name}_label']}))
        return fieldsets

    class Meta:
        model = Price
        fields = '__all__'