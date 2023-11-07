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



# для отзыва на помошника
