from django import forms
from django.contrib.contenttypes.forms import generic_inlineformset_factory
from django.utils.translation import gettext as _
import articles
from .models import Helper, ReviewHelper, ReviewArt_Event, Like
from events.models import Article, Event, Tag_article
from accounts.models import *
from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.contenttypes.models import ContentType
from helpySamui.constants import REGION_CHOICES, LANGUAGE_CHOICES, LEVEL_CHOICES, TAG_ARTICLE_CHOICES, \
    REVIEW_RATING_CHOICES, TAG_HELP_NAME_CHOICES


class ReviewHelperCreateForm(forms.ModelForm):
    class Meta:
        model = ReviewHelper
        fields = ["reviewer_name", "helper_name", "rating", "tag", "level_of_service", "review_text", "wishes"]
        labels = {
            "reviewer_name": _("Reviewer Name"),
            "helper_name": _("Helper Name"),
            "rating": _("Rating"),
            "tag": _("Tag"),
            "level_of_service": _("Level of Service"),
            "review_text": _("Review Text"),
            "wishes": _("Wishes"),
        }
        widgets = {
            "rating": forms.NumberInput(attrs={"min": 1, "max": 5}),
            "tag": forms.Select(choices=TAG_HELP_NAME_CHOICES),
            "level_of_service": forms.Select(choices=LEVEL_CHOICES),
        }

class ReviewHelperEditForm(forms.ModelForm):
    class Meta:
        model = ReviewHelper
        fields = ["reviewer_name", "helper_name", "rating", "tag", "level_of_service", "review_text", "wishes"]
        labels = {
            "reviewer_name": _("Your Name"),
            "helper_name": _("Helper's Name"),
            "rating": _("Rating"),
            "tag": _("Tag"),
            "level_of_service": _("Level of Service"),
            "review_text": _("Review Text"),
            "wishes": _("Wishes"),
        }
        widgets = {
            "rating": forms.NumberInput(attrs={"min": 1, "max": 5}),
            "level_of_service": forms.RadioSelect(choices=LEVEL_CHOICES),
            "tag": forms.RadioSelect(choices=TAG_HELP_NAME_CHOICES),
        }
class ReviewForm_Art_Event(forms.ModelForm):
    REVIEW_TYPES = [
        ('article', 'Article'),
        ('event', 'Event'),
    ]
    review_type = forms.ChoiceField(choices=REVIEW_TYPES)
    content_id = forms.IntegerField()
    reviewer_name = forms.CharField(max_length=255)
    comment = forms.CharField(widget=forms.Textarea)
    rating = forms.IntegerField(widget=forms.NumberInput(attrs={'min': 1, 'max': 5}))
    relevance = forms.IntegerField(widget=forms.NumberInput(attrs={'min': 1, 'max': 5}))
    engagement = forms.IntegerField(widget=forms.NumberInput(attrs={'min': 1, 'max': 5}))

    class Meta:
        model = ReviewArt_Event
        fields = ['review_type', 'content_id', 'reviewer_name', 'comment', 'rating', 'relevance', 'engagement']

    def clean(self):
        cleaned_data = super().clean()
        review_type = cleaned_data.get('review_type')
        content_id = cleaned_data.get('content_id')

        if review_type == 'article':
            try:
                Article.objects.get(pk=content_id)
            except Article.DoesNotExist:
                raise forms.ValidationError('Article does not exist')
        elif review_type == 'event':
            try:
                Event.objects.get(pk=content_id)
            except Event.DoesNotExist:
                raise forms.ValidationError('Event does not exist')
        else:
            raise forms.ValidationError('Invalid review type')

        return cleaned_data
class ReviewFormEdit_Art_Event(forms.ModelForm):
    REVIEW_TYPES = [
        ('article', 'Article'),
        ('event', 'Event'),
    ]
    review_type = forms.ChoiceField(choices=REVIEW_TYPES)
    content_id = forms.IntegerField()
    reviewer_name = forms.CharField(max_length=255)
    comment = forms.CharField(widget=forms.Textarea)
    rating = forms.IntegerField(widget=forms.NumberInput(attrs={'min': 1, 'max': 5}))
    relevance = forms.IntegerField(widget=forms.NumberInput(attrs={'min': 1, 'max': 5}))
    engagement = forms.IntegerField(widget=forms.NumberInput(attrs={'min': 1, 'max': 5}))

    class Meta:
        model = ReviewArt_Event
        fields = ['review_type', 'content_id', 'reviewer_name', 'comment', 'rating', 'relevance', 'engagement']

    def clean(self):
        cleaned_data = super().clean()
        review_type = cleaned_data.get('review_type')
        content_id = cleaned_data.get('content_id')

        if review_type == 'article':
            try:
                Article.objects.get(pk=content_id)
            except Article.DoesNotExist:
                raise forms.ValidationError('Article does not exist')
        elif review_type == 'event':
            try:
                Event.objects.get(pk=content_id)
            except Event.DoesNotExist:
                raise forms.ValidationError('Event does not exist')
        else:
            raise forms.ValidationError('Invalid review type')

        return cleaned_data


class ArticleModerationForm(forms.ModelForm):
    action = forms.ChoiceField(choices=(('approve', 'Approve'), ('edit', 'Edit'), ('delete', 'Delete')))

    class Meta:
        model = Article
        fields = ['title', 'content']


class EventModerationForm(forms.ModelForm):
    CHOICES = [
        ('approve', 'Approve'),
        ('edit', 'Edit'),
        ('delete', 'Delete'),
    ]
    action = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())

    class Meta:
        model = Event
        fields = ['title', 'description', 'location']


class ReviewHelperModerationForm(forms.ModelForm):
    CHOICES = [
        ('approve', 'Approve'),
        ('edit', 'Edit'),
        ('delete', 'Delete'),
    ]
    action = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())

    class Meta:
        model = ReviewHelper
        fields = ['reviewer_name', 'helper_name', 'review_text', 'wishes']


class ReviewArtEventModerationForm(forms.ModelForm):
    CHOICES = [
        ('approve', 'Approve'),
        ('edit', 'Edit'),
        ('delete', 'Delete'),
    ]
    action = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())

    class Meta:
        model = ReviewArt_Event
        fields = ['review_type', 'content_id', 'reviewer_name', 'comment', 'rating', 'relevance', 'engagement']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content_id'].widget.attrs['readonly'] = True

    def clean_content_id(self):
        content_id = self.cleaned_data['content_id']
        review_type = self.cleaned_data['review_type']
        if review_type == 'article':
            content_type = ContentType.objects.get_for_model(Article)
        elif review_type == 'event':
            content_type = ContentType.objects.get_for_model(Event)
        else:
            raise forms.ValidationError('Invalid review type')
        try:
            content_object = content_type.get_object_for_this_type(id=content_id)
        except content_type.model_class().DoesNotExist:
            raise forms.ValidationError('Invalid content id')
        self.cleaned_data['content_object'] = content_object
        return content_id

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance


ReviewArtEventModerationFormset = generic_inlineformset_factory(
    ReviewArt_Event,
    form=ReviewArtEventModerationForm,
    extra=0,
    can_delete=False,
)






