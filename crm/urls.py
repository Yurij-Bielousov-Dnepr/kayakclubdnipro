from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import RedirectView
from views import ( BookingCreateView, BookingCancelView, BookingUpdateView, BookingView, BookingList, BookingSearch,)


urlpatterns = [
    path("", RedirectView.as_view(pattern_name="helpy:index", permanent=False)),
    path("/crm/booking/create/", BookingCreateView.as_view(), name="booking-create",),
        # **Коментар:** Створює нову бронь  **Заголовок:** Створення броні
    path("/crm/booking/cancel/<int:id>/", BookingCancelView.as_view(), name="booking-cancel",),
        # **Коментар:** Скасовує бронь з ідентифікатором <id> **Заголовок:** Скасування броні
    path("/crm/booking/update/<int:id>/", BookingUpdateView.as_view(), name="booking-update", ),
        # **Коментар:** Змінює бронювання з ідентифікатором <id>**Заголовок:** Редагування броні
    path("/crm/booking/view/<int:id>/", BookingView.as_view(), name="booking-view",),
        # **Коментар:** Переглядає бронювання з ідентифікатором <id>**Заголовок:** Перегляд броні
    path("/crm/booking/list/", BookingList.as_view(), name="booking-list", ),
        # **Коментар:** Повертає список всіх бронювань**Заголовок:** Список бронювань
    path("/crm/booking/search/", BookingSearch.as_view(), name="booking-search",),
        # **Коментар:** Повертає список бронювань, які відповідають заданим критеріям пошуку **Заголовок:** Пошук бронювань
    path("date/<date>/", BookingList.as_view(), name="booking-list-by-date",),
        # **Коментар:** Повертає список бронювань, датованих `<date>` **Заголовок:** Список бронювань за датою
    path("client/<int:id>/", BookingList.as_view(), name="booking-list-by-client",),
        # **Коментар:** Повертає список бронювань клієнта з ідентифікатором `<id>`**Заголовок:** Список бронювань за клієнтом
    path("product/<int:id>/", BookingList.as_view(), name="booking-list-by-product",),
        # **Коментар:** Повертає список бронювань товару з ідентифікатором `<id>`**Заголовок:** Список бронювань за товаром
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# \
#    \
#     + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# if settings.DEBUG:    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


