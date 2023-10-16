# models.py
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

from accounts.models import MyUser
from offer.models import Helper
from events.models import Article, Event
from helpySamui.constants import REGION_CHOICES, LANGUAGE_CHOICES, LEVEL_CHOICES, TAG_ARTICLE_CHOICES, \
    REVIEW_RATING_CHOICES
from django.contrib.contenttypes.models import ContentType


class Like(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    is_like = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


# для отзыва на помошника
class ReviewHelper(models.Model):

    reviewer_name = models.CharField(max_length=255)
    helper_name = models.CharField(max_length=255)
    rating = models.PositiveSmallIntegerField(choices=REVIEW_RATING_CHOICES)
    tag = models.CharField(choices=TAG_ARTICLE_CHOICES, max_length=100, blank=False)
    level_of_service = models.PositiveSmallIntegerField(choices=LEVEL_CHOICES)
    review_text = models.TextField()
    wishes = models.TextField(blank=True)
    is_approved = models.BooleanField(default=False)
    likes = GenericRelation(Like)

    def get_like_url(self):
        return reverse('like_toggle', args=[self.pk, self.__class__.__name__.lower()])

    def __str__(self):
        return f"Review for {self.helper_name} by {self.reviewer_name}"



    # Review - для отзыва на статью или событие
class ReviewArt_Event(models.Model):
    REVIEW_TYPES = [
        ('article', 'Article'),
        ('event', 'Event'),
    ]
    review_type = models.CharField(max_length=10, choices=REVIEW_TYPES)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    reviewer_name = models.CharField(max_length=255)
    comment = models.TextField()
    rating = models.IntegerField(choices=REVIEW_RATING_CHOICES)
    relevance = models.IntegerField(choices=REVIEW_RATING_CHOICES, verbose_name="Relevance")
    engagement = models.IntegerField(choices=REVIEW_RATING_CHOICES, verbose_name="Engagement")
    likes = GenericRelation(Like)

    def get_like_url(self):
        return reverse('like_toggle', args=[self.pk, self.__class__.__name__.lower()])

    def save(self, *args, **kwargs):
        if not self.id:
            if self.review_type == 'article':
                self.content_type = ContentType.objects.get_for_model(Article)
            elif self.review_type == 'event':
                self.content_type = ContentType.objects.get_for_model(Event)
        super().save(*args, **kwargs)
