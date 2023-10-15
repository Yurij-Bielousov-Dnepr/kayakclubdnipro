from django.apps import AppConfig


class BookingCayakConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'booking_cayak'
    verbose_name = 'Booking Cayak'

    # def ready(self):
    #     from .models import BoatType
    #     BoatType.create_from_constants()