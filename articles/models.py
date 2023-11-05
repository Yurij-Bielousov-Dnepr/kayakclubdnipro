# models.py
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from booking_cayak.models import Tag
from django.contrib.contenttypes.models import ContentType
from booking_cayak.models import MyUser


class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    rating = models.IntegerField(default=0)
    is_approved = models.BooleanField(default=False)
    is_favorite = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, verbose_name="Tags",  blank=False)

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


# для отзыва на помошника
