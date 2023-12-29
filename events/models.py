# models.py
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from crm.models import MyUser


class Trip(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    length_in_days = models.IntegerField()
    description = models.TextField()
    organizer = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    place = models.CharField(max_length=255, blank=True, null=True)
    maximum_participants = models.IntegerField(blank=True, null=True)
    registration = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Тріп'
        verbose_name_plural = 'Тріпи'

    def __str__(self):
        return f"Тріп: {self.date}, {self.start_time}, {self.length_in_days}"


class Event(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    length_in_hours = models.IntegerField()
    description = models.TextField()
    organizer = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    place = models.CharField(max_length=255, blank=True, null=True)
    maximum_participants = models.IntegerField(blank=True, null=True)
    registration = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Подія'
        verbose_name_plural = 'Події'

    def __str__(self):
        return f"Подія: {self.date}, {self.start_time}, {self.length_in_hours}"




