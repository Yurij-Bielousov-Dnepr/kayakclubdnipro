from datetime import datetime
from django.utils import timezone
from django.db import models
from django.core.exceptions import ValidationError
from .constants import BOAT_TYPES


class BoatType(models.Model):
    type_name = models.CharField(max_length=100, verbose_name='Назва типу')
    quantity = models.PositiveIntegerField(verbose_name='Кількість', default=1)
    image = models.CharField(max_length=100, verbose_name='Шлях до зображення')
    description = models.TextField(verbose_name='Опис')
    details = models.TextField(verbose_name='Деталі')

    def __str__(self):
        return self.type_name

    @classmethod
    def create_from_constants(cls):
        for boat_type_data in BOAT_TYPES:
            cls.objects.create(
                type_name=boat_type_data['name'],
                quantity=boat_type_data['quantity'],
                image=boat_type_data['image'],
                description=boat_type_data['description'],
                details=boat_type_data['details']
            )
    class Meta:
        verbose_name_plural = "Типи лодок"

class Boat(models.Model):
    boat_type = models.ForeignKey(BoatType, on_delete=models.CASCADE, null=True, default=None, verbose_name="Тип лодки")
    boat_index = models.PositiveIntegerField(verbose_name="Індекс лодки", default=1)
    nickname = models.CharField(max_length=100, verbose_name='Призвісько')
    bookings = models.ManyToManyField('Booking', through='BoatBooking', verbose_name="Обрані човни", blank=True,
                                      related_name="booked_boats")
    STATUS_CHOICES = [
        ('F', 'Вільний'),
        ('C', 'В обробці'),
        ('B', 'Зайнятий'),
    ]
    status = models.CharField(max_length=1, default="F", choices=STATUS_CHOICES, verbose_name="Статус")

    def __str__(self):
        return f"{self.boat_type.type_name} № {self.boat_index} відома як: {self.nickname} має статус - {self.get_status_display()}"

    class Meta:
        verbose_name_plural = "Лодки:"


class BoatStatus(models.Model):
    STATUS_CHOICES = [
        ('F', 'Вільний'),
        ('C', 'В обробці'),
        ('B', 'Зайнятий'),
    ]

    boat = models.ForeignKey(Boat, on_delete=models.CASCADE, verbose_name="Лодка")
    start_time = models.DateTimeField(default=datetime(2022, 2, 24, 4, 0), blank=True, null=True, verbose_name="Час початку")
    end_time = models.DateTimeField(default=datetime(2022, 2, 24, 6, 0), null=True, blank=True, verbose_name="Час закінчення")
    status = models.CharField(default='F', max_length=1, choices=STATUS_CHOICES, verbose_name="Статус")

    def __str__(self):
        return f"{self.boat} - {self.get_status_display()} ({self.start_time} - {self.end_time})"

    class Meta:
        verbose_name_plural = "Статус лодок"


class Price(models.Model):
    DURATION_CHOICES = [
        ('30m', '30 хвилин'),
        ('1h', '1 година'),
        ('2h', '2 години'),
        ('3h', '3 години'),
        ('4h', '4 години'),
        ('5h', '5 годин'),
        ('5-7h', '5-7 годин'),
        ('7-12h', '7-12 годин'),
        ('24h', '24 години'),
    ]

    capacity_1 = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Ціна за годину (1 особа)", blank=True, null=True)
    capacity_1_label = models.CharField(max_length=100, verbose_name="Надпис (1 особа)", default="Ціна за годину (1 особа)")

    capacity_2 = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Ціна за годину (2 особи)", blank=True, null=True)
    capacity_2_label = models.CharField(max_length=100, verbose_name="Надпис (2 особи)", default="Ціна за годину (2 особи)")

    capacity_3 = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Ціна за годину (3 особи)", blank=True, null=True)
    capacity_3_label = models.CharField(max_length=100, verbose_name="Надпис (3 особи)", default="Ціна за годину (3 особи)")

    price_per_hour = models.DecimalField(max_digits=8, decimal_places=2)

    duration = models.CharField(max_length=10, choices=DURATION_CHOICES, verbose_name="Тривалість")

    def get_price_for_capacity(self, capacity):
        if capacity == 1:
            return self.capacity_1
        elif capacity == 2:
            return self.capacity_2
        elif capacity == 3:
            return self.capacity_3
        # Додайте аналогічні умови для решти колонок
        return None

    def __str__(self):
        return f"Тривалість: {self.get_duration_display()} - Ціни: {self.capacity_1}, {self.capacity_2}, {self.capacity_3}"

    class Meta:
        verbose_name_plural = "Ціни:"


    def get_rental_price(self):
        price = Price.objects.get(boat_type=self.boat_status.boat.boat_type, duration=self.duration)
        return price.price_per_hour * self.duration

    rental_price = property(get_rental_price)

    def calculate_total_price(self):
        price = Price.objects.get(boat_type=self.boat_status.boat.boat_type, duration=self.duration)
        total_price = price.price_per_hour * self.duration
        if self.discount == 'DR':
            total_price -= total_price * 0.1
        elif self.discount == 'SOU':
            total_price -= price.price_per_hour
        elif self.discount == 'Volunteer' or self.discount == 'Refugee':
            discount_amount = min(total_price * 0.5, price.price_per_hour * 2)
            total_price -= discount_amount
        return total_price

    class Meta:
         verbose_name_plural = "Бронювання"

class Review(models.Model):

    reviewer_name = models.CharField(max_length=255)
    name_service = models.CharField(max_length=255)
    RATING_CHOICES = (
        (1, '1 звезда'),
        (2, '2 звезды'),
        (3, '3 звезды'),
        (4, '4 звезды'),
        (5, '5 звезд'),
    )

    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    TAG_ARTICLE_CHOICES = (
        (TAG_ARTICLE_MOTO_RENT, 'Moto Rent'),
        (TAG_ARTICLE_MOTO_BEGINNER, 'Moto Beginner'),
        (TAG_ARTICLE_MOTO_SOS, 'Moto SOS'),
        (TAG_ARTICLE_RENT_ESTATE, 'Rent Estate'),
        (TAG_ARTICLE_PUBLIC_SERV, 'Public Service'),
        (TAG_ARTICLE_LANG_SCHOL, 'Language School'),
        (TAG_ARTICLE_MED_HELP, 'Medical Help'),
        (TAG_ARTICLE_SERV_TRANSL, 'Translation Services'),
        (TAG_ARTICLE_SHOPPING_DESTINATION, 'Shopping Destination'),
        (TAG_ARTICLE_SOUVENIRS, 'Souvenirs'),
    )
    tag = models.CharField(choices=TAG_ARTICLE_CHOICES, max_length=100, blank=False)
    review_text = models.TextField()
    wishes = models.TextField(blank=True)
    is_approved = models.BooleanField(default=False)
    likes = GenericRelation(Like)

    def get_like_url(self):
        return reverse('like_toggle', args=[self.pk, self.__class__.__name__.lower()])

    def __str__(self):
        return f"Review for {self.helper_name} by {self.reviewer_name}"