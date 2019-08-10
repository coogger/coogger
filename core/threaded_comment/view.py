from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, reverse
from django.views.generic import TemplateView, UpdateView
from django_page_views.models import DjangoViews
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from django.contrib.contenttypes.models import ContentType

from core.cooggerapp.views.utils import model_filter

from .forms import ReplyForm
from .models import ThreadedComments
from .serializers import ReplySerializer


class ReplyView(TemplateView):
    template_name = "reply-detail.html"
    model = ThreadedComments
    form_class = ReplyForm
    model_name = "threadedcomments"
    app_label = "threaded_comment"

    def save_view(self, request, id):  # TODO use reqeust/response signals
        # TODO same code in /cooggerapp/generic/detail.py
        get_view, created = DjangoViews.objects.get_or_create(
            content_type=ContentType.objects.get(
                app_label=self.app_label, model=self.model_name
            ),
            object_id=id,
        )
        try:
            get_view.ips.add(request.ip_model)
        except IntegrityError:
            pass

    def get_context_data(self, username, permlink, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class
        context["current_user"] = User.objects.get(username=username)
        context["queryset"] = self.model.objects.get(
            user__username=username, permlink=permlink
        )
        self.save_view(self.request, context["queryset"].id)
        return context


class ReplyUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = ThreadedComments
    fields = ["body"]
    template_name = "content/post/update.html"
    success_message = "Your reply updated"

    def get_object(self):
        permlink = self.kwargs.get("permlink")
        return get_object_or_404(self.model, user=self.request.user, permlink=permlink)

    def get_success_url(self):
        return reverse(
            "reply-detail",
            kwargs=dict(
                username=self.kwargs.get("username"),
                permlink=self.kwargs.get("permlink"),
            ),
        )


# rest api
class ListReply(ListCreateAPIView):
    model = ThreadedComments
    serializer_class = ReplySerializer
    permission_classes = []

    def get_object(self):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        return self.model.objects.all().order_by("created")

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)

    def filter_queryset(self, queryset):
        return model_filter(self.request.query_params.items(), self.get_queryset()).get(
            "queryset"
        )
