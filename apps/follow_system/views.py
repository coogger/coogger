from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views import View
from rest_framework.generics import ListCreateAPIView
from rest_framework.serializers import ModelSerializer, SlugRelatedField

from .models import Follow as FollowModel


class Follow(LoginRequiredMixin, View):
    def get(self, request, username):
        from_user = User.objects.get(username=request.user.username)
        to_user = User.objects.get(username=username)
        if (
            FollowModel.objects.filter(user=from_user)
            .filter(following=to_user)
            .exists()
        ):
            status = "unfollow"
            from_user.follow.following.remove(to_user)
        else:
            status = "follow"
            from_user.follow.following.add(to_user)
        return JsonResponse(
            dict(status=status, from_user=str(from_user), to_user=str(to_user))
        )


class GetFollower(LoginRequiredMixin, ListCreateAPIView):
    class FollowSerializer(ModelSerializer):
        following = SlugRelatedField(
            many=True, read_only=True, slug_field="username"
        )
        follower = SlugRelatedField(
            many=True, read_only=True, slug_field="username"
        )

        class Meta:
            model = FollowModel
            fields = ("username", "following", "follower")

    model = FollowModel
    serializer_class = FollowSerializer
    permission_classes = []

    def get_queryset(self):
        username = self.request.GET.get("username", None)
        if username is None:
            user = self.request.user
        else:
            user = User.objects.get(username=username)
        return self.model.objects.filter(user=user)
