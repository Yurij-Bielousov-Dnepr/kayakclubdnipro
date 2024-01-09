from django.urls import path
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from django.contrib import admin

# from telegram_bot.views import webhook, telegram_bot
# from telegram_bot.telegram_bot import set_webhook, webhook
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.admin.views.decorators import staff_member_required
from . import views
from .views import Events_detail
from .views import event_list, event_detail, create_event, edit_event


app_name = "art_event"  # добавьте это, если используете пространства имен
urlpatterns = [
    path('events/', event_list, name='event_list'),
    path('events/<int:pk>/', event_detail, name='event_detail'),
    path('events/create/', create_event, name='create_event'),
    path('events/<int:pk>/edit/', edit_event, name='edit_event'),
    path('events/<int:pk>/', Events_detail.as_view(), name='event_detail'),
    path("events/add/", views.EventCreateView.as_view(), name="add_event"),
    path(
        "events/<int:pk>/update/",
        views.EventUpdateView.as_view(),
        name="update_event",
    ),
    path(
        "events/<int:pk>/delete/",
        views.EventDeleteView.as_view(),
        name="delete_event",
    ),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
