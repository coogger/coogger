# django
from django.http import Http404
from django.views.generic.base import TemplateView

# models
from ..models import Content, Topic, Category

# views
from ..views.utils import model_filter

# choices
from ..choices import LANGUAGES

# utils
from .utils import paginator


class TopicView(TemplateView):
    template_name = "topic/index.html"

    def get_context_data(self, permlink, *args, **kwargs):
        queryset = Content.objects.filter(utopic__permlink=permlink, status="approved", reply=None)
        if queryset.exists():
            context = super().get_context_data(**kwargs)
            context["queryset"] = paginator(self.request, queryset)
            context["topic"] = Topic.objects.get(permlink=permlink)
            context["topic_users"] = self.get_users(queryset)
            return context
        raise Http404

    def get_users(self, queryset):
        users = []
        for query in queryset:
            if query.user not in users:
                users.append(query.user)
                if len(users) == 30:
                    break
        return users


class Hashtag(TemplateView):
    template_name = "card/blogs.html"

    def get_context_data(self, hashtag, **kwargs):
        queryset = Content.objects.filter(tags__contains=hashtag, status="approved", reply=None)
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
            queryset = Content.objects.filter(language=lang_name, status="approved", reply=None)
            context = super().get_context_data(**kwargs)
            context["queryset"] = paginator(self.request, queryset)
            context["language"] = lang_name
            return context
        raise Http404


class Categories(TemplateView):
    template_name = "card/blogs.html"

    def get_context_data(self, cat_name, **kwargs):
        queryset = Content.objects.filter(
            category__name=cat_name, status="approved", reply=None
        )
        context = super().get_context_data(**kwargs)
        context["queryset"] = paginator(self.request, queryset)
        context["category"] = cat_name
        return context


class Filter(TemplateView):
    template_name = "card/blogs.html"
    model = Content

    def get_context_data(self, **kwargs):
        queryset = self.model.objects.filter(status="approved", reply=None)
        filtered = model_filter(self.request.GET.items(), queryset)
        queryset = filtered.get("queryset")
        context = super().get_context_data(**kwargs)
        context["queryset"] = paginator(self.request, queryset)
        context["filter"] = filtered.get("filter")
        return context
