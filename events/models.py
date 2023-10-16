# models.py
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
# from django.contrib.auth.models import User
from accounts.models import MyUser
from helpySamui.constants import REVIEW_RATING_CHOICES, TAG_ARTICLE_CHOICES, TAG_HELP_NAME_CHOICES


class Tag_article(models.Model):
    name = models.CharField(max_length=20, choices=TAG_ARTICLE_CHOICES)

    def __str__(self):
        return self.get_name_display()

    class Meta:
        app_label = 'art_event'


class Event(models.Model):
    title = models.CharField(max_length=55)
    description = models.CharField(max_length=255)
    date = models.DateField()
    location = models.CharField(max_length=155)
    rating = models.IntegerField(default=0)
    is_approved = models.BooleanField(default=False)
    is_favorite = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag_article, verbose_name="Tags", blank=False)

    # def clean(self):
    #     super().clean()
    #     for tag in self.tags.all():
    #         if tag.name not in dict(TAG_ARTICLE_CHOICES).keys():
    #             raise ValidationError(f"Tag '{tag.name}' is not a valid choice.")
    #


class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    rating = models.IntegerField(default=0)
    is_approved = models.BooleanField(default=False)
    is_favorite = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag_article, verbose_name="Tags",  blank=False)

    # def clean(self):
    #     super().clean()
    #     for tag in self.tags.all():
    #         if tag.name not in dict(TAG_ARTICLE_CHOICES).keys():
    #             raise ValidationError(f"Tag '{tag.name}' is not a valid choice.")


class Review(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    reviewer_name = models.CharField(max_length=255)
    comment = models.TextField()
    rating = models.IntegerField(choices=REVIEW_RATING_CHOICES)
    relevance = models.IntegerField(choices=REVIEW_RATING_CHOICES, verbose_name="Relevance")
    engagement = models.IntegerField(choices=REVIEW_RATING_CHOICES, verbose_name="Engagement")

class Favorites(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, null=True, blank=True
    )
    is_favorite = models.BooleanField(default=False)


