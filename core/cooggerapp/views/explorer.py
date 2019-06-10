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
        topic = Topic.objects.filter(permlink=permlink)[0]
        queryset = Content.objects.filter(utopic__permlink=permlink, status="approved", reply=None)
        if queryset.exists():
            context = super().get_context_data(**kwargs)
            context["queryset"] = paginator(self.request, queryset)
            topic_query = Topic.objects.filter(name=topic)
            if topic_query.exists():
                context["topic"] = topic_query[0]
                context["topic_users"] = self.get_users(queryset)
            else:
                Topic(name=topic).save()
            return context
        raise Http404

    def get_users(self, queryset):
        users = []
        for query in queryset:
            if query.user.username not in users:
                users.append(query.user.username)
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
            context["nameofhashtag"] = hashtag
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
        category = Category.objects.filter(name=cat_name)
        if category.exists():
            queryset = Content.objects.filter(
                category=category[0], status="approved", reply=None
            )
            context = super().get_context_data(**kwargs)
            context["queryset"] = paginator(self.request, queryset)
            context["category"] = cat_name
            return context
        raise Http404


class Filter(TemplateView):
    template_name = "card/blogs.html"
    queryset = Content.objects.filter(status="approved", reply=None)

    def get_context_data(self, **kwargs):
        filtered = model_filter(self.request.GET.items(), self.queryset)
        context = super().get_context_data(**kwargs)
        context["queryset"] = paginator(self.request, filtered.get("queryset"))
        context["filter"] = filtered.get("filter")
        return context
