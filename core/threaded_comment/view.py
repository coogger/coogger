from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django_page_views.models import DjangoViews
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response

from core.cooggerapp.views.utils import model_filter

from .forms import ReplyForm
from .models import ThreadedComments
from .serializers import ReplySerializer


class ReplyView(TemplateView):
    template_name = "reply-detail.html"
    model = ThreadedComments
    form_class = ReplyForm

    def get_context_data(self, username, permlink, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class
        context["current_user"] = User.objects.get(username=username)
        context["queryset"] = self.model.objects.get(
            user__username=username, permlink=permlink
        )
        return context


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
