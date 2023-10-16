from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext as _
from .models import Article, Event, Tag_article
# from accounts.models import
from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "content", "tags"]

        widgets = {
            "content": forms.Textarea(),
            "tags": forms.CheckboxSelectMultiple(attrs={"class": "checkbox"}),
        }


class EventCreationForm(forms.ModelForm):
    date = forms.DateField(widget=forms.SelectDateWidget)
    time = forms.CharField(max_length=5, widget=forms.TimeInput(format="%H:%M"))
    location = forms.CharField(max_length=255)
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag_article.objects.all(), widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Event
        fields = ["title", "description", "date", "time", "location", "tags"]


class EventCreateView(CreateView):
    model = Event
    template_name = "art_event/add_event.html"
    form_class = EventCreationForm
    success_url = reverse_lazy("events")

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'tags', 'location']

class EventUpdateView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'art_event/event_Update.html'
    success_url = '/events/'

# EventCreationForm - форма для создания нового события.
# EventForm - форма для обновления существующего события.
# ArticleForm - форма для создания новой статьи.