from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.views.generic import ListView

from ...models import Content, SearchedWords, UTopic


class Search(ListView):
    user_template_name = "home/search/user.html"
    content_template_name = "home/search/content.html"
    utopic_template_name = "home/search/utopic.html"
    not_result_template_name = "home/search/not_result.html"
    valid_search = {"@": "user", "#": "utopic"}

    def get_template_names(self):
        query = self.request.GET["query"].lower()
        if query and len(query) > 3:
            if query[0] in self.valid_search:
                return [getattr(self, f"{self.valid_search[query[0]]}_template_name")]
        if not self.object_list.exists():
            return [self.not_result_template_name]
        return [self.content_template_name]

    def get_queryset(self):
        query = self.request.GET["query"].lower()
        if query and len(query) > 3:
            SearchedWords(word=query).save()  # TODO use request signal
            if query[0] in self.valid_search:
                return getattr(self, self.valid_search[query[0]])(query[1:])
            return self.content(query)
        else:
            messages.warning(
                self.request,
                "Please enter your search key with min 4 characters or more.",
            )
        return Content.objects.none()

    def user(self, query):
        queryset = User.objects.filter(
            Q(is_active=True),
            Q(username__contains=query)
            | Q(first_name__contains=query)
            | Q(last_name__contains=query),
        )
        return queryset

    def content(self, query):
        return Content.objects.filter(Q(title__contains=query) & Q(status="ready"))

    def utopic(self, query):
        return UTopic.objects.filter(name__contains=query)
