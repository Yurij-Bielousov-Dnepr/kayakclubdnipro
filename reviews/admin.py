from django.contrib import admin
from reviews.models import ReviewHelper, ReviewArt_Event


@admin.register(ReviewArt_Event)
class ReviewArtEventAdmin(admin.ModelAdmin):
    pass

@admin.register(ReviewHelper)
class ReviewHelperAdmin(admin.ModelAdmin):
    pass