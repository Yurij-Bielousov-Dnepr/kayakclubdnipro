from django.contrib import admin
from crm.models import Review, Event, Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'rating', 'is_approved')
    list_filter = ('is_approved',)
    search_fields = ('title', 'tags__name')


