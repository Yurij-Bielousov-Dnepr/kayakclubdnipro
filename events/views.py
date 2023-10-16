# views.py
from datetime import date

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views
from django_countries import countries
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.forms import ModelForm
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext as _
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .decorators import admin_only
from .forms import *
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# from .forms import HelperForm
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView, TemplateView
from django.views.generic.edit import FormView, CreateView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login
from .my_menu import *
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views import View


# Классы-представления для статей (Article)
class ArticleListView(ListView):
    model = Article
    template_name = "art_event/articles.html"
    context_object_name = "articles"

class Events_detail(DetailView):
    model = Event
    template_name = "art_event/event_detail.html"
    context_object_name = "event"

def events(request):
    events = Event.objects.order_by("date")[:3]
    context = {"events": events}
    return render(request, "art_event/events.html", context)

def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["events"] = Event.objects.all()
    return context
class EventCreateView(CreateView):
    model = Event
    template_name = "art_event/add_event.html"
    form_class = EventCreateView
    fields = ("title", "description", "date", "location", "tags", "is_favorite")
    success_url = reverse_lazy("events")

    # fields = ( 'Calendar', 'Events Calendar', 'Google Maps',)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        return context


class EventUpdateView(View):
    def get(self, request, *args, **kwargs):
        event = get_object_or_404(Event, pk=kwargs["pk"])
        form = EventForm(instance=event)
        return render(request, "art_event/event_Update.html", {"form": form})

    def post(self, request, *args, **kwargs):
        event = get_object_or_404(Event, pk=kwargs["pk"])
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect("event_detail", pk=event.pk)
        return render(request, "art_event/event_Update.html", {"form": form})


class EventDeleteView(DeleteView):
    model = Event
    template_name = "art_event/event_confirm_delete.html"
    success_url = reverse_lazy("events")


@login_required  # Ограничиваем доступ только для авторизованных пользователей
def favorites(request):
    user = request.user
    # Получаем список статей и событий, которые пользователь добавил в избранное
    favorite_articles = Article.objects.filter(favorites=user.profile)
    favorite_events = Event.objects.filter(favorites=user.profile)
    context = {
        "favorite_articles": favorite_articles,
        "favorite_events": favorite_events,
    }
    return render(request, "art_event/favorites.html", context)


def add_article(request):
    form = ArticleForm()
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            # сохраняем данные из формы в базу данных
            form.save()
            # редиректим пользователя на другую страницу
            return redirect("articles")
    return render(request, "art_event/add_article.html", {"form": form})


class ArticleUpdateView(UpdateView):
    model = Article
    template_name = "art_event/article_Update.html"
    fields = (
        "title",
        "content",
    )
    success_url = reverse_lazy("article_list")


def add_event(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            return redirect("event_detail", pk=event.pk)
    else:
        form = EventForm()
    return render(request, "art_event/add_event.html", {"form": form})


def articles(request):
    return render(request, "art_event/articles.html")


class ArticleFormView:
    def get(self, request, *args, **kwargs):
        return render(request, "art_event/articles.html")


# class ArticleDetailView:
#     pass
