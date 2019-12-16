from core.follow_system.templatetags.follow_system_tags import (
    follower_count, following_count, is_follow
)
from django.contrib.auth.models import User
from django.test import TestCase


class FollowTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username="user1")
        self.user2 = User.objects.create(username="user2")
        self.user1.follow.following.add(self.user2)

    def test_login(self):
        url = "/follow/get/"
        response = self.client.get(url)
        self.assertEqual(response.url, f"/accounts/login/?next={url}")

    def test_login2(self):
        url = "/follow/%40user12/"
        response = self.client.get(url)
        self.assertEqual(response.url, f"/accounts/login/?next={url}")

    def test_following_list(self):
        following_list = self.user1.follow.following.all()
        self.assertEqual(following_list[0], self.user2)

    def test_is_follow(self):
        is_follow = self.user1.follow.is_follow(self.user2)
        self.assertEqual(is_follow, True)


class TemplateTagTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username="user1")
        self.user2 = User.objects.create(username="user2")
        self.user1.follow.following.add(self.user2)

    def test_following_count(self):
        user = User.objects.get(username="user1")
        self.assertEqual(following_count(user), 1)

    def test_follower_count(self):
        user = User.objects.get(username="user1")
        self.assertEqual(follower_count(user), 0)

    def test_is_follow(self):
        user = User.objects.get(username="user1")
        other_user = User.objects.get(username="user2")
        self.assertEqual(is_follow(user, other_user), True)
