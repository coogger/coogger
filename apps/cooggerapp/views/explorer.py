from django.conf import settings
from django.views.generic import ListView

from ..models import Content, Topic
from ..views.utils import model_filter


class ExplorerMixin(ListView):
    model = Content
    not_result_template_name = "home/search/not_result.html"
    paginate_by = 10
    ordering = "-created"
    http_method_names = ["get"]

    def get_template_names(self):
        if self.object_list.exists():
            return [self.template_name]
        else:
            return [self.not_result_template_name]

    def dispatch(self, request, *args, **kwargs):
        "Set attribute as a class variable the keywords in URL."
        for key, value in self.kwargs.items():
            setattr(self, key, value)
        return super().dispatch(request, *args, **kwargs)


class TopicView(ExplorerMixin):
    template_name = "topic/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["topic"] = Topic.objects.get(permlink=self.permlink)
        context["topic_users"] = self.get_users(self.object_list)
        return context

    def get_queryset(self):
        return self.model.objects.filter(
            utopic__permlink=self.permlink, status="ready", utopic__status="public"
        ).order_by(self.ordering)

    def get_users(self, queryset):
        users = set()
        for query in queryset:
            users.add(query.user)
            if len(users) == settings.USERS_PER_TOPIC:
                break
        return users


class Hashtag(ExplorerMixin):
    template_name = "card/blogs.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hashtag"] = self.hashtag
        return context

    def get_queryset(self):
        return self.model.objects.filter(
            tags__contains=self.hashtag, status="ready", utopic__status="public"
        ).order_by(self.ordering)


class Languages(ExplorerMixin):
    template_name = "card/blogs.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["language"] = self.language
        return context

    def get_queryset(self):
        return self.model.objects.filter(
            language=self.language, status="ready", utopic__status="public"
        ).order_by(self.ordering)


class Filter(ExplorerMixin):
    template_name = "card/blogs.html"
    extra_context = dict(filter=True)  # filtered.get("filter")

    def get_queryset(self):
        queryset = self.model.objects.filter(status="ready").order_by(self.ordering)
        return (
            model_filter(self.request.GET.items(), queryset)
            .get("queryset")
            .filter(utopic__status="public")
        )
