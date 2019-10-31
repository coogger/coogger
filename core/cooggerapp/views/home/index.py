from django.conf import settings
from django.contrib.auth.models import User
from django.urls import resolve
from django.views.generic import ListView

from ...models import Content, Issue, Topic, UTopic


class Index(ListView):
    template_name = "card/blogs.html"
    introduction_template_name = "home/introduction.html"
    not_result_template_name = "home/search/not_result.html"
    paginate_by = 10
    http_method_names = ["get"]
    introduction = False
    extra_context = dict(insection_left=True, insection_right=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.introduction:
            context.update(
                utopics=UTopic.objects.all()
                .order_by("-how_many")
                .distinct()[: settings.PAGE_SIZE]
            )
        else:
            context.update(
                issues=Issue.objects.filter(status="open")[: settings.PAGE_SIZE],
                sort_topics=self.sort_topics(),
            )
        return context

    def get_queryset(self):
        if (
            not self.request.user.is_authenticated
            and resolve(self.request.path_info).url_name == "index"
        ):
            self.introduction = True
            self.paginate_by = None
            return User.objects.filter(is_active=True).order_by("-date_joined")[:24]
        else:
            return Content.objects.filter(user__is_active=True, status="ready")

    def get_template_names(self):
        if not self.object_list.exists():
            return [self.not_result_template_name]
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
