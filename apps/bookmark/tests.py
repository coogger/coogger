from django.contrib.auth.models import User
from django.test import TestCase

from .templatetags.apps.bookmark import how_many_mark, is_mark


class BookmarkTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user("test1", "test1@test.com", "111111")

    def test_bookmark_save(self):
        self.client.login(username=self.user1.username, password="111111")
        add_or_remove = self.client.post(
            "/bookmark/add_or_remove/",
            {"app_label": "auth", "model": "permission", "object_id": "1"},
        )
        self.assertEqual(add_or_remove.content, b'{"status": true}')

        add_or_remove = self.client.post(
            "/bookmark/add_or_remove/",
            {"app_label": "auth", "model": "permission", "object_id": "1"},
        )
        self.assertEqual(add_or_remove.content, b'{"status": false}')


class TemplateTagTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user("test1", "test1@test.com", "111111")
        self.user2 = User.objects.create_user("test2", "test1@test.com", "111111")

    def test_is_mark_none(self):
        self.assertEqual(is_mark(self.user1, User, 2), False)

    def test_is_mark_true(self):
        self.client.login(username=self.user1.username, password="111111")
        add_or_remove = self.client.post(
            "/bookmark/add_or_remove/",
            {"app_label": "auth", "model": "user", "object_id": "2"},
        )
        self.assertEqual(is_mark(self.user1, User, 2), True)

    def test_is_mark_false(self):
        self.test_is_mark_true()
        add_or_remove = self.client.post(
            "/bookmark/add_or_remove/",
            {"app_label": "auth", "model": "user", "object_id": "2"},
        )
        self.assertEqual(is_mark(self.user1, User, 2), False)

    def test_how_many_mark(self):
        self.test_is_mark_true()
        self.client.login(username=self.user2.username, password="111111")
        add_or_remove = self.client.post(
            "/bookmark/add_or_remove/",
            {"app_label": "auth", "model": "user", "object_id": "2"},
        )
        how_many = how_many_mark(self.user1, 2)
        self.assertEqual(how_many, 2)
