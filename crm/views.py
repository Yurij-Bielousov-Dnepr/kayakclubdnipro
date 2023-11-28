from django.shortcuts import render
from django.shortcuts import render, redirect
from django.views.generic import CreateView, DeleteView, UpdateView, ListView, DetailView
from .models import Booking

class BookingCreateView(CreateView):
    model = Booking
    template_name = 'crm/create.html'
    fields = ['date', 'time', 'client', 'product', 'is_confirmed']

    def get_success_url(self):
        return redirect('booking-list')

class BookingCancelView(DeleteView):
    model = Booking
    template_name = 'crm/cancel.html'
    success_url = '/crm/booking/list'

class BookingUpdateView(UpdateView):
    model = Booking
    template_name = 'crm/update.html'
    fields = ['date', 'time', 'client', 'product', 'is_confirmed']

    def get_success_url(self):
        return redirect('booking-list')

class BookingView(DetailView):
    model = Booking
    template_name = 'crm/view.html'

class BookingList(ListView):
    model = Booking
    template_name = 'crm/list.html'

    def get_queryset(self):
        queryset = Booking.objects.all()
        date = self.request.GET.get('date')
        client_id = self.request.GET.get('client_id')
        product_id = self.request.GET.get('product_id')

        if date:
            queryset = queryset.filter(date=date)
        if client_id:
            queryset = queryset.filter(client_id=client_id)
        if product_id:
            queryset = queryset.filter(product_id=product_id)

        return queryset

class BookingSearch(ListView):
    model = Booking
    template_name = 'crm/search.html'

    def get_queryset(self):
        queryset = Booking.objects.all()
        search_term = self.request.GET.get('search_term')

        if search_term:
            queryset = queryset.filter(
                Q(client__name__icontains=search_term) |
                Q(product__name__icontains=search_term)
            )

        return queryset