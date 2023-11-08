from django.contrib import admin
from crm.models import Article, Event, Tag, Review, Favorite


#    from .models import Favorites,


# @admin.register(Article)
# class ArticleAdmin(admin.ModelAdmin):

#     def formfield_for_manytomany(self, db_field, request, **kwargs):
#         if db_field.name == 'tags':
#             kwargs['queryset'] = Tag_article.objects.all().order_by('name')
#         return super().formfield_for_manytomany(db_field, request, **kwargs)
#
# @admin.register(Event)
# class EventAdmin(admin.ModelAdmin):
#     pass
#     def formfield_for_manytomany(self, db_field, request, **kwargs):
#         if db_field.name == 'tags':
#             kwargs['queryset'] = Tag_article.objects.all().order_by('name')
#         return super().formfield_for_manytomany(db_field, request, **kwargs)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    ordering = ('name',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'date', 'is_approved')
    list_filter = ('is_approved',)
    search_fields = ('title', 'location', 'tags__name')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'article', 'reviewer_name', 'rating', 'relevance', 'engagement')
    list_filter = ('rating', 'relevance', 'engagement')
    search_fields = ('article__title', 'reviewer_name')


@admin.register(Favorite)
class FavoritesAdmin(admin.ModelAdmin):
    pass


