from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Vote
from .templatetags.vote import downvote_count, is_vote, upvote_count


def get_content_type(app_label, model):
    return ContentType.objects.get(app_label=app_label, model=model)


def get_model(app_label, model):
    content_type_obj = ContentType.objects.get(app_label=app_label, model=model)
    return content_type_obj.model_class()


class DjangoVoteSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Vote
        fields = ("username", "status")
        read_only_fields = ["status"]


class VoteView(View):
    @method_decorator(login_required)
    def post(self, request, app_label, model, id):
        if request.POST.get("status") == "false":
            status = False
        elif request.POST.get("status") == "true":
            status = True
        try:
            Vote(
                user=self.request.user,
                content_type=get_content_type(app_label, model),
                object_id=id,
                status=status,
            ).save()
        except ValidationError as e:
            return HttpResponse(JsonResponse({"error": str(e)}))
        model = get_model(app_label=app_label, model=model)
        return HttpResponse(
            JsonResponse(
                {
                    "status": is_vote(self.request.user, model, id),
                    "upvote_count": upvote_count(model, id),
                    "downvote_count": downvote_count(model, id),
                }
            )
        )


class GetVotes(APIView):

    serializer_class = DjangoVoteSerializer
    permission_classes = []

    def get(self, request, app_label, model, id):
        queryset = Vote.objects.filter(
            content_type=get_content_type(app_label, model), object_id=id
        )
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class IsVote(View):
    def get(self, request, username, app_label, model, id):
        user = User.objects.get(username=username)
        model = get_model(app_label=app_label, model=model)
        return HttpResponse(JsonResponse({"status": is_vote(user, model, id)}))
