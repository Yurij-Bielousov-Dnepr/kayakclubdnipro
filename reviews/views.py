# views.py
# from .forms import HelperForm
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST
from django.views.generic import ListView, UpdateView
from django.views.generic.edit import CreateView
from .models import Like
import reviews.models
from .decorators import admin_only
from .forms import *
from reviews.models import *
from .forms import ArticleModerationForm, EventModerationForm, ReviewHelperModerationForm


@login_required
@require_POST
@login_required
@require_POST
def like(request):
    content_type_id = request.POST.get('content_type_id')
    object_id = request.POST.get('object_id')
    value = request.POST.get('value')

    # Получаем тип модели
    content_type = get_object_or_404(ContentType, pk=content_type_id)

    # Получаем модель и объект по id
    model_class = content_type.model_class()
    obj = get_object_or_404(model_class, id=object_id)

    # Получаем лайк для данного пользователя и объекта
    like_obj, created = Like.objects.get_or_create(content_type=content_type, object_id=object_id, user=request.user)

    # Устанавливаем значение лайка и сохраняем
    like_obj.value = value
    like_obj.save()

    # Получаем количество лайков и дизлайков
    likes_count = Like.objects.filter(content_type=content_type, object_id=object_id, value=True).count()
    dislikes_count = Like.objects.filter(content_type=content_type, object_id=object_id, value=False).count()

    # Возвращаем json с данными о количестве лайков и дизлайков
    return JsonResponse({'likes_count': likes_count, 'dislikes_count': dislikes_count})


@login_required
def ReviewHelperEdit(request, pk):
    review_helper = get_object_or_404(ReviewHelper, pk=pk)

    if request.user != review_helper.reviewer_name and not request.user.is_staff:
        raise Http404(_("You are not allowed to access this page."))

    if request.method == "POST":
        form = ReviewHelperEditForm(request.POST, instance=review_helper)
        if form.is_valid():
            review_helper = form.save()
            return redirect("review_helper_detail", pk=review_helper.pk)
    else:
        form = ReviewHelperEditForm(instance=review_helper)

    return render(request, "reviews/review_helper_edit.html", {"form": form})


@login_required
def review_edit(request, review_id):
    review = get_object_or_404(ReviewArt_Event, pk=review_id)

    if request.method == 'POST':
        form = ReviewForm_Art_Event(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
    else:
        form = ReviewFormEdit_Art_Event(instance=review)

    context = {
        'form': form,
        'review': review,
    }

    return render(request, 'reviews/review_edit.html', context)


# тут надо разобраться модернизировать вьюху чтобы она модерила все: статьи, события и отзывы
@staff_member_required
def moderation_view(request):
    article_form = ArticleModerationForm()
    event_form = EventModerationForm()
    review_form = ReviewHelperModerationForm()

    if request.method == 'POST':
        article_id = request.POST.get('article_id')
        event_id = request.POST.get('event_id')
        review_id = request.POST.get('review_id')

        if article_id:
            article = get_object_or_404(Article, pk=article_id)
            article_form = ArticleModerationForm(request.POST, instance=article)
            if article_form.is_valid():
                if article_form.cleaned_data['action'] == 'approve':
                    article.is_approved = True
                    article.save()
                elif article_form.cleaned_data['action'] == 'edit':
                    article.save()
                    return redirect('edit_article', pk=article.pk)
                elif article_form.cleaned_data['action'] == 'delete':
                    article.delete()

        if event_id:
            event = get_object_or_404(Event, pk=event_id)
            event_form = EventModerationForm(request.POST, instance=event)
            if event_form.is_valid():
                if event_form.cleaned_data['action'] == 'approve':
                    event.is_approved = True
                    event.save()
                elif event_form.cleaned_data['action'] == 'edit':
                    event.save()
                    return redirect('edit_event', pk=event.pk)
                elif event_form.cleaned_data['action'] == 'delete':
                    event.delete()

        if review_id:
            review = get_object_or_404(ReviewHelper, pk=review_id)
            review_form = ReviewHelperModerationForm(request.POST, instance=review)
            if review_form.is_valid():
                if review_form.cleaned_data['action'] == 'approve':
                    review.is_approved = True
                    review.save()
                elif review_form.cleaned_data['action'] == 'edit':
                    review.save()
                    return redirect('edit_review', pk=review.pk)
                elif review_form.cleaned_data['action'] == 'delete':
                    review.delete()

        if request.POST.get('event_approve'):
            event = get_object_or_404(Event, pk=request.POST.get('event_approve'))
            event.is_approved = True
            event.save()

        if request.POST.get('review_approve'):
            review = get_object_or_404(ReviewArt_Event, pk=request.POST.get('review_approve'))
            review.is_approved = True
            review.save()

        articles = Article.objects.filter(is_approved=False)
        events = Event.objects.filter(is_approved=False)
        reviews = ReviewHelper.objects.filter(is_approved=False)

        return render(request, "moderation.html", {
            "articles": articles,
            "events": events,
            "reviews": reviews,
            "article_form": article_form,
            "event_form": event_form,
            "review_form": review_form,
        })


class ReviewCreateView(CreateView):
    model = ReviewHelper
    form_class = ReviewHelperCreateForm
    template_name = "reviews/review_add.html"
    success_url = reverse_lazy("reviews:thanks")

    def form_valid(self, form):
        review = form.save(commit=False)
        review.customer_name = form.cleaned_data.get("customer_name")
        review.helper_name = form.cleaned_data.get("helper_name")
        review.rating = form.cleaned_data.get("rating")
        review.tag = form.cleaned_data.get("tag")
        review.level_of_service = form.cleaned_data.get("level_of_service")
        review.review_text = form.cleaned_data.get("review_text")
        review.wishes = form.cleaned_data.get("wishes")
        review.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ReviewHelperCreateForm()
        return context


@login_required
def review_helper_edit(request, pk):
    """
    Представление для редактирования отзыва о помощнике
    """
    review = get_object_or_404(ReviewHelper, pk=pk)
    if not request.user.is_staff and review.reviewer_name != request.user:
        return redirect('review_helper_detail', pk=review.pk)
    if request.method == 'POST':
        form = ReviewHelperEditForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('review_helper_detail', pk=review.pk)
    else:
        form = ReviewHelperEditForm(instance=review)
    return render(request, 'reviews/review_helper_edit.html', {'form': form})


def review_helper(request):
    context = {
        "page_title": _("User Reviews"),
        "page_description": _(
            "User reviews are important for evaluating the quality and usability of the website. Sorting and adding reviews are important components of the user experience. They allow users to quickly find the information they need and share their opinion. It is important to ensure the security of reviews by checking for spam and moderation."
        ),
        "add_review_url": "reviews_add",
        "reviews_list_url": "reviews_list",
    }
    return render(request, "reviews/review_helper.html", context)


def review_list_helper(request):
    reviews = ReviewHelper.objects.all()

    sort_by = request.GET.get("sort", "rating")
    sort_order = request.GET.get("order", "desc")

    if sort_order == "desc":
        sort_by = f"-{sort_by}"

    reviews = reviews.order_by(sort_by)

    paginator = Paginator(reviews, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "reviews": page_obj,
        "sort_by": sort_by,
    }
    return render(request, "reviews/reviews_list.html", context)


def review_detail(request, pk):
    review = get_object_or_404(ReviewHelper, pk=pk)
    context = {
        "review": review,
    }
    return render(request, "reviews/reviews_detail.html", context)

def review_list(request):
    reviews = ReviewArt_Event.objects.all()
    order = request.GET.get("order", "-created_at")
    paginator = Paginator(reviews.order_by(order), 9)
    page = request.GET.get("page")
    reviews = paginator.get_page(page)
    context = {"reviews": reviews, "order": order}
    return render(request, "reviews/reviews_list.html", context=context)


def ReviewCreateArt_Event(request):
    if request.method == "POST":
        form = ReviewForm_Art_Event(request.POST)
        if form.is_valid():
            helper_nick = form.cleaned_data["helper_nick"]
            category_help = form.cleaned_data["category_help"]
            problem_description = form.cleaned_data["problem_description"]
            rate = form.cleaned_data["rate"]
            comment = form.cleaned_data["comment"]
            helper = Helper.objects.get(name=helper_nick)
            ReviewArt_Event.objects.create(
                helper=helper,
                category_help=category_help,
                problem_description=problem_description,
                rate=rate,
                comment=comment,
            )
            return redirect("reviews")
    else:
        form = ReviewForm_Art_Event()
    return render(request, "reviews/review_add.html", {"form": form})

def create_review_Art_Event(request):
   if request.method == 'POST':
        form = ReviewForm_Art_Event(request.POST)
        if form.is_valid():
            review_type = form.cleaned_data.get('review_type')
            content_id = form.cleaned_data.get('content_id')
            reviewer_name = form.cleaned_data.get('reviewer_name')
            comment = form.cleaned_data.get('comment')
            rating = form.cleaned_data.get('rating')
            relevance = form.cleaned_data.get('relevance')
            engagement = form.cleaned_data.get('engagement')

            if review_type == 'article':
                try:
                    content_object = Article.objects.get(pk=content_id)
                except ObjectDoesNotExist:
                    form.add_error('content_id', 'Invalid article id')
                    return render(request, 'review_add.html', {'form': form})

            elif review_type == 'event':
                try:
                    content_object = Event.objects.get(pk=content_id)
                except ObjectDoesNotExist:
                    form.add_error('content_id', 'Invalid event id')
                    return render(request, 'review_add.html', {'form': form})
            else:
                form.add_error('review_type', 'Invalid review type')
                return render(request, 'review_add.html', {'form': form})

            review = ReviewArt_Event(
                review_type=review_type,
                content_object=content_object,
                reviewer_name=reviewer_name,
                comment=comment,
                rating=rating,
                relevance=relevance,
                engagement=engagement,
            )
            review.save()

            return render(request, 'review_add.html', {'review': review})
        else:
            form = ReviewForm_Art_Event()
        return render(request, 'review_add.html', {'form': form})
