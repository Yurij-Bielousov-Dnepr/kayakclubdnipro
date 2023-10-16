from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import RedirectView


urlpatterns = [
    path("", RedirectView.as_view(pattern_name="helpy:index", permanent=False)),

    path("admin/", admin.site.urls),
    path("helpy/", include("helpy.urls")),
    path("offer/", include("offer.urls")),
    path("reviews/", include("reviews.urls")),
    path("accounts/", include("allauth.urls")),
    path("art_event/", include("art_event.urls")),
    path("accounts/", include("accounts.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# \
#    \
#     + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# if settings.DEBUG:    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# path('offer-help/', views.offer_help, name='offer_help'),
# path('telegram-bot/', views.telegram_bot, name='telegram_bot'),
# path('events/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
# path('article/form/', ArticleFormView.as_view(), name='article_form'),path('addhelper', views.Helper),
# path('articles/', views.ArticleListView.as_view(), name='article_list'),
# path('articles/<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail'),
# path('articles/create/', views.ArticleCreateView.as_view(), name='article_create'),
# path('articles/<int:pk>/update/', views.ArticleUpdateView.as_view(), name='article_update'),
# path('articles/<int:pk>/delete/', views.ArticleDeleteView.as_view(), name='article_delete'),
# path('events/', views.EventListView.as_view(), name='event_list'),
# path('events/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
# path('events/create/', views.EventCreateView.as_view(), name='event_create'),
# path('events/<int:pk>/update/', views.EventUpdateView.as_view(), name='event_update'),
# path('events/<int:pk>/delete/', views.EventDeleteView.as_view(), name='event_delete'),
# path('helpers/', views.HelperListView.as_view(), name='helper_list'),
# path('helpers/<int:pk>/', views.HelperDetailView.as_view(), name='helper_detail'),
# path('helpers/create/', views.HelperCreateView.as_view(), name='helper_create'),
# path('helpers/<int:pk>/update/', views.HelperUpdateView.as_view(), name='helper_update'),
# path('helpers/<int:pk>/delete/', views.HelperDeleteView.as_view(), name='helper_delete'),
# path('events/', events, name='events'),
