from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from booking_cayak.constants import BOAT_TYPES, RATING_CHOICES, DURATION_CHOICES, TAG_CHOICES
from booking_cayak.models import BoatStatus, Boat


class MyUser(User):
    # Історія бронювань
    bookings = models.ManyToManyField(
        "bookings.Booking",
        related_name="users",
        verbose_name="Історія бронювань",
    )

    # Вподобані статті
    liked_articles = models.ManyToManyField(
        "articles.Article",
        related_name="users",
        verbose_name="Вподобані статті",
    )

    # Вподобані події
    liked_events = models.ManyToManyField(
        "events.Event",
        related_name="users",
        verbose_name="Вподобані події",
    )

    # Відгуки, які написав користувач
    reviews = models.ManyToManyField(
        "reviews.Review",
        related_name="users",
        verbose_name="Відгуки, які написав користувач",
    )


class Booking(models.Model):
    date = models.DateField()
    time = models.TimeField()
    client = models.ForeignKey('MyUser.Client', on_delete=models.CASCADE)
    BookingBoat = models.ForeignKey('BookingBoat.Boat', on_delete=models.CASCADE)
    is_confirmed = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Бронювання'
        verbose_name_plural = 'Бронювання'

# Уточнить поля модели  Бронирования  1 Бронюваннялієнт/орендувач
# 2 Тип ПЗ
# 3 Ціну оренди обраного ПЗ 4 Колл ПЗ
# 5 Обрати пільгу: ДР, 6 Цена итого 7 Инфа в коммент
class BookingHistory(models.Model):
    status = models.CharField(max_length=1, choices=[('C', 'В обробці'), ('B', 'Затверджено'), ('R', 'Відхилено')],
                              verbose_name="Статус бронювання")
    rent_date = models.DateField(verbose_name="Дата прокату")
    User_History = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name="Користувач")
    start_time = models.DateTimeField(verbose_name="Час початку")
    end_time = models.DateTimeField(verbose_name="Час закінчення")


class Tag(models.Model):
    code = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)


# class Article(models.Model):
#     title = models.CharField(max_length=255)
#     content = models.TextField()
#     rating = models.IntegerField(default=0)
#     is_approved = models.BooleanField(default=False)
#     is_favorite = models.BooleanField(default=False)
#     tags = models.ManyToManyField(Tag, verbose_name="Tags",  blank=False, related_name="Tags")

    # def clean(self):
    #     super().clean()
    #     for tag in self.tags.all():
    #         if tag.name not in dict(TAG_ARTICLE_CHOICES).keys():
    #             raise ValidationError(f"Tag '{tag.name}' is not a valid choice.")


class Like(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    is_like = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Event(models.Model):
    title = models.CharField(max_length=55)
    description = models.CharField(max_length=255)
    date = models.DateField()
    location = models.CharField(max_length=155)
    rating = models.IntegerField(default=0)
    is_approved = models.BooleanField(default=False)
    is_favorite = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, related_name="reviews")

    # def clean(self):
    #     super().clean()
    #     for tag in self.tags.all():
    #         if tag.name not in dict(TAG_ARTICLE_CHOICES).keys():
    #             raise ValidationError(f"Tag '{tag.name}' is not a valid choice.")
    #


class Favorite(models.Model):
    """Модель для зберігання вподобань користувача."""

    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    content_type = models.ForeignKey(
        "contenttypes.ContentType", on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField()
    is_favorite = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Вподобання"
        verbose_name_plural = "Вподобання"

    def __str__(self):
        return f"{self.user} - {self.content_type} - {self.object_id}"


class Review(models.Model):
    reviewer_name = models.CharField(max_length=255)
    name_service = models.CharField(max_length=255)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    tags = models.ManyToManyField(Tag, related_name="reviews")
    review_text = models.TextField(max_length=255)
    wishes = models.TextField(blank=True)
    is_approved = models.BooleanField(default=False)
    likes = GenericRelation(Like)

    def get_like_url(self):
        return reverse('like_toggle', args=[self.pk, self.__class__.__name__.lower()])

    def __str__(self):
        return f"Відгук від {self.reviewer_name} що використав послугу {self.name_service}"
