from django.conf import settings
from django.contrib.auth.models import User
from django.urls import resolve
from django.views.generic import ListView

from ...forms import ReportsForm
from ...models import Content, Issue, ReportModel, SearchedWords, Topic
from ..utils import paginator


class Index(ListView):
    template_name = "card/blogs.html"
    introduction_template_name = "home/introduction.html"
    not_result_template_name = "home/search/not_result.html"
    paginate_by = 10
    http_method_names = ["get"]
    introduction = False
    extra_context = dict(insection_left=True, insection_right=True)

    def dispatch(self, request, *args, **kwargs):
        "Set attribute as a class variable the keywords in URL."
        for key, value in self.kwargs.items():
            setattr(self, key, value)
        if (
            not self.request.user.is_authenticated
            and resolve(self.request.path_info).url_name == "index"
        ):
            self.introduction = True
            self.paginate_by = None
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sort_topics"] = self.sort_topics()  # TODO just pc
        context["issues"] = Issue.objects.filter(status="open")[: settings.PAGE_SIZE]
        return context

    def get_queryset(self):
        if self.introduction:
            return User.objects.filter(is_active=True).order_by("-date_joined")[:24]
        else:
            return Content.objects.filter(user__is_active=True, status="ready")

    def get_template_names(self):
        if not self.object_list.exists():
            [self.not_result_template_name]
        elif self.introduction:
            return [self.introduction_template_name]
        else:
            return [self.template_name]

    @staticmethod
    def sort_topics():
        topics = list()
        for topic in Topic.objects.all():
            if (topic not in topics) and (len(topics) <= 30) and (not topic.editable):
                topics.append(topic)
        return topics
