from django.urls import path
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView, CreateView
from django.contrib import admin
# from telegram_bot.views import webhook, telegram_bot
# from telegram_bot.telegram_bot import set_webhook, webhook
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.admin.views.decorators import staff_member_required
from .forms import ReviewForm_Art_Event
from .models import ReviewArt_Event
from .views import (
    review_helper,
    ReviewCreateView,
    review_edit,
    moderation_view,
    review_list_helper,
    review_detail, review_helper_edit, ReviewHelperEdit, ReviewCreateArt_Event, like, moderation_view,
)

app_name = "reviews"  # добавьте это, если используете пространства имен

urlpatterns = [
    path("reviews/review_helper/", review_helper, name="review_helper"),
    path( 'review_edit/<int:pk>/', review_edit, name='review_edit_Art_Event' ),
    path("reviews/add/", CreateView.as_view(model=ReviewArt_Event, form_class=ReviewForm_Art_Event),
         name="review-add_Art_Event"),
    path( "reviews/", review_list_helper, name="reviews_list" ),
    path("reviews/<int:pk>/", review_detail, name="review_detail"),
    path("reviews/moderate/",
        staff_member_required(moderation_view), name="moderation_view", ),
    path("<int:pk>/", review_detail, name="review_detail"),
    path("add/", ReviewCreateView.as_view(), name="reviews_add"),
    path("<int:pk>/edit/", ReviewHelperEdit, name="review_edit"),
    path('post/<int:pk>/like/', like, name='post_like'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT).as_view()
