from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'booking_cayak'


urlpatterns = [
    path('booking/', views.booking, name='booking'),
    path('booking/success/', views.booking_success, name='booking_success'),
    path('crm/', views.booking_crm, name='crm'),
    path('assortment/', TemplateView.as_view(template_name='assortment.html'), name='assortment'),
    path('', TemplateView.as_view(template_name='Index.html'), name='index'),
    path('price/', TemplateView.as_view(template_name='price.html'), name='price'),
    path('routes/', TemplateView.as_view(template_name='routes.html'), name='routes'),
]