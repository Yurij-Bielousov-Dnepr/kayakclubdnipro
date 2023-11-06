from django.db import models
from booking_cayak.models import MyUser


class BookingHistory(models.Model):
    status = models.CharField(max_length=1, choices=[('C', 'В обробці'), ('B', 'Затверджено'), ('R', 'Відхилено')],
                              verbose_name="Статус бронювання")
    rent_date = models.DateField(verbose_name="Дата прокату")
    User_History = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name="Користувач")
    start_time = models.DateTimeField(verbose_name="Час початку")
    end_time = models.DateTimeField(verbose_name="Час закінчення")