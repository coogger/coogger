# django
from django.http import Http404

# django class based
from django.views.generic.base import TemplateView

# models
from core.cooggerapp.models import Content, Topic, CategoryofDapp

# views
from core.cooggerapp.utils import paginator, content_by_filter

# choices
from core.cooggerapp.choices import languages


class TopicView(TemplateView):
    template_name = "topic/index.html"

    def get_context_data(self, topic, *args, **kwargs):
        queryset = Content.objects.filter(topic=topic, status="approved")
        if queryset.exists():
            info_of_cards = paginator(self.request, queryset)
            context = super(TopicView, self).get_context_data(**kwargs)
            context["content"] = info_of_cards
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
            if query.username not in users:
                users.append(query.username)
                if len(users) == 30:
                    break
        return users


class Hashtag(TemplateView):
    template_name = "card/blogs.html"

    def get_context_data(self, hashtag, **kwargs):
        queryset = Content.objects.filter(tags__contains=hashtag, status="approved")
        if queryset.exists():
            info_of_cards = paginator(self.request, queryset)
            context = super(Hashtag, self).get_context_data(**kwargs)
            context["content"] = info_of_cards
            context["nameofhashtag"] = hashtag
            return context
        raise Http404


class Languages(TemplateView):
    template_name = "card/blogs.html"

    def get_context_data(self, lang_name, **kwargs):
        if lang_name in languages:
            queryset = Content.objects.filter(language=lang_name, status="approved")
            info_of_cards = paginator(self.request, queryset)
            context = super(Languages, self).get_context_data(**kwargs)
            context["content"] = info_of_cards
            context["language"] = lang_name
            return context
        raise Http404


class Categories(TemplateView):
    template_name = "card/blogs.html"

    def get_context_data(self, cat_name, **kwargs):
        if CategoryofDapp.objects.filter(name=cat_name).exists():
            queryset = Content.objects.filter(
                category=cat_name, status="approved"
            )
            context = super(Categories, self).get_context_data(**kwargs)
            info_of_cards = paginator(self.request, queryset)
            context["content"] = info_of_cards
            context["category"] = cat_name
            return context
        raise Http404


class Filter(TemplateView):
    template_name = "card/blogs.html"
    queryset = Content.objects.filter(status="approved")

    def get_context_data(self, **kwargs):
        filtered = content_by_filter(self.request.GET.items(), self.queryset)
        context = super(Filter, self).get_context_data(**kwargs)
        context["content"] = paginator(self.request, filtered.get("queryset"))
        context["filter"] = filtered.get("filter")
        return context
