from .models import Helper, HelpRequest, User, Stats
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out
from datetime import date


@receiver(post_save, sender=Helper)
@receiver(post_delete, sender=Helper)
def update_active_helpers_count(sender, **kwargs):
    active_helpers_count = Helper.objects.filter(user_offer_is_free=True).count()
    stats, _ = Stats.objects.get_or_create(date=date.today())
    stats.active_helpers = active_helpers_count
    stats.save()


@receiver(post_save, sender=HelpRequest)
@receiver(post_delete, sender=HelpRequest)
def update_help_requests_count(sender, **kwargs):
    help_requests_count = HelpRequest.objects.count()
    stats, _ = Stats.objects.get_or_create(date=date.today())
    stats.help_requests = help_requests_count
    stats.save()


@receiver(user_logged_in)
@receiver(user_logged_out)
def update_online_users_count(sender, request, user, **kwargs):
    online_users_count = User.objects.filter(is_authenticated=True).count()
    stats, _ = Stats.objects.get_or_create(date=date.today())
    stats.online_users = online_users_count
    stats.save()
