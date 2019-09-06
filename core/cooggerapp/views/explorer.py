from django.http import Http404
from django.views.generic import TemplateView

from ..choices import LANGUAGES
from ..models import Content, Topic
from ..views.utils import model_filter
from .utils import paginator


class TopicView(TemplateView):
    template_name = "topic/index.html"

    def get_context_data(self, permlink, *args, **kwargs):
        queryset = Content.objects.filter(utopic__permlink=permlink, status="ready")
        context = super().get_context_data(**kwargs)
        context["queryset"] = paginator(self.request, queryset)
        context["topic"] = Topic.objects.get(permlink=permlink)
        context["topic_users"] = self.get_users(queryset)
        return context

    def get_users(self, queryset):
        users = set()
        for query in queryset:
            users.add(query.user)
            if len(users) == 30:
                break
        return users


class Hashtag(TemplateView):
    template_name = "card/blogs.html"

    def get_context_data(self, hashtag, **kwargs):
        queryset = Content.objects.filter(tags__contains=hashtag, status="ready")
        if queryset.exists():
            context = super().get_context_data(**kwargs)
            context["queryset"] = paginator(self.request, queryset)
            context["hashtag"] = hashtag
            return context
        raise Http404


class Languages(TemplateView):
    template_name = "card/blogs.html"

    def get_context_data(self, lang_name, **kwargs):
        if lang_name in LANGUAGES:
            queryset = Content.objects.filter(language=lang_name, status="ready")
            context = super().get_context_data(**kwargs)
            context["queryset"] = paginator(self.request, queryset)
            context["language"] = lang_name
            return context
        raise Http404


class Categories(TemplateView):
    template_name = "card/blogs.html"

    def get_context_data(self, cat_name, **kwargs):
        queryset = Content.objects.filter(category__name=cat_name, status="ready")
        context = super().get_context_data(**kwargs)
        context["queryset"] = paginator(self.request, queryset)
        context["category"] = cat_name
        return context


class Filter(TemplateView):
    template_name = "card/blogs.html"
    model = Content

    def get_context_data(self, **kwargs):
        queryset = self.model.objects.filter(status="ready")
        filtered = model_filter(self.request.GET.items(), queryset)
        queryset = filtered.get("queryset")
        context = super().get_context_data(**kwargs)
        context["queryset"] = paginator(self.request, queryset)
        context["filter"] = filtered.get("filter")
        return context
