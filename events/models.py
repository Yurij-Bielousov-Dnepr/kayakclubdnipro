# models.py
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from booking_cayak.models import MyUser
from booking_cayak.models import Tag


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



# class Favorites(models.Model):
    #    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    #    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
    #    article = models.ForeignKey(
    #        Article, on_delete=models.CASCADE, null=True, blank=True
    #     )
    #    is_favorite = models.BooleanField(default=False)


