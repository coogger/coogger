import os

from django.contrib.auth.models import User
from django.test import TestCase

from .models import Badges, UserBadge


class BadgeTest(TestCase):
    image_address = f"{os.getcwd()}/badge/image/python.jpg"

    def setUp(self):
        self.user1 = User.objects.create_user("test1", "test1@test.com", "111111")
        self.badge, created = Badges.objects.get_or_create(
            title="python", image_address=self.image_address
        )
        self.user_badge, created = UserBadge.objects.get_or_create(user=self.user1)

    def test_user_add_badge(self):
        add_new_badge = self.user_badge.badge.add(self.badge)
        self.assertEqual(add_new_badge, None)
