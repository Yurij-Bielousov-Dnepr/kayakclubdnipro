from django.apps import AppConfig


# class MyAppConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'art_event'
#
#     def ready(self):
#         from art_event.models import Tag_article
#
#         # удаляем все записи в модели Tag_article
#         Tag_article.objects.all().delete()
#
#         # создаем новые записи для каждого значения в списке TAG_ARTICLE_CHOICES
#         for choice in TAG_ARTICLE_CHOICES:
#             Tag_article.objects.create(name=choice[1])


class ArtEventConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "events"
