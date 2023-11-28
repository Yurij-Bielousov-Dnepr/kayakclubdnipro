from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import RedirectView
from views import (
    BookingCreateView,
    BookingCancelView,
    BookingUpdateView,
    BookingView,
    BookingList,
    BookingSearch,
)



urlpatterns = [
    path("", RedirectView.as_view(pattern_name="helpy:index", permanent=False)),
        /crm/booking/create
Коментар: Забронювати: Створює нову бронь
    /crm/booking/cancel/<id>
Коментар: Скасовує бронь з ідентифікатором <id>

/crm/booking/update/<id>
Коментар: Змінює бронь з ідентифікатором <id>
/crm/booking/view/<id>
Коментар: Переглядає бронь з ідентифікатором <id>
/crm/booking/list
Коментар: Повертає список всіх бронювань
/crm/booking/search
Коментар: Повертає список бронювань, які відповідають заданим критеріям пошуку


urlpatterns = [
    # **Основні URL-адреси**

    # **Створення броні**
    path(
        "create/",
        BookingCreateView.as_view(),
        name="booking-create",
        # **Коментар:** Створює нову бронь
        # **Заголовок:** Створення броні
    ),

    # **Скасування броні**
    path(
        "cancel/<int:id>/",
        BookingCancelView.as_view(),
        name="booking-cancel",
        # **Коментар:** Скасовує бронь з ідентифікатором <id>
        # **Заголовок:** Скасування броні
    ),

    # **Зміна бронювання**
    path(
        "update/<int:id>/",
        BookingUpdateView.as_view(),
        name="booking-update",
        # **Коментар:** Змінює бронювання з ідентифікатором <id>
        # **Заголовок:** Редагування броні
    ),

    # **Перегляд бронювання**
    path(
        "view/<int:id>/",
        BookingView.as_view(),
        name="booking-view",
        # **Коментар:** Переглядає бронювання з ідентифікатором <id>
        # **Заголовок:** Перегляд броні
    ),

    # **Список бронювань**
    path(
        "list/",
        BookingList.as_view(),
        name="booking-list",
        # **Коментар:** Повертає список всіх бронювань
        # **Заголовок:** Список бронювань
    ),

    # **Пошук бронювань**
    path(
        "search/",
        BookingSearch.as_view(),
        name="booking-search",
        # **Коментар:** Повертає список бронювань, які відповідають заданим критеріям пошуку
        # **Заголовок:** Пошук бронювань
    ),

    # **Додаткові URL-адреси**

    # **Список бронювань за датою**
    path(
        "date/<date>/",
        BookingList.as_view(),
        name="booking-list-by-date",
        # **Коментар:** Повертає список бронювань, датованих `<date>`
        # **Заголовок:** Список бронювань за датою
    ),

    # **Список бронювань за клієнтом**
    path(
        "client/<int:id>/",
        BookingList.as_view(),
        name="booking-list-by-client",
        # **Коментар:** Повертає список бронювань клієнта з ідентифікатором `<id>`
        # **Заголовок:** Список бронювань за клієнтом
    ),

    # **Список бронювань за товаром**
    path(
        "product/<int:id>/",
        BookingList.as_view(),
        name="booking-list-by-product",
        # **Коментар:** Повертає список бронювань товару з ідентифікатором `<id>`
        # **Заголовок:** Список бронювань за товаром
    ),
]
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
