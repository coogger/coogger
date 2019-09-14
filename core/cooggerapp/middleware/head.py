from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.urls import resolve
from django.utils.deprecation import MiddlewareMixin

from ...threaded_comment.models import ThreadedComments
from ..models import Commit, Content, Topic, UserProfile, UTopic


class HeadMixin:
    invalid = ["sitemap", "api", "robots.txt", "admin", "static", "media"]
    default_img = "https://www.coogger.com/static/logos/png/800.png"
    default_hashtag_img = "/static/media/icons/list.svg"
    default_language_img = "/static/media/topics/language.svg"

    def process_request(self, request):
        path_info = request.path_info
        if path_info.split("/")[1] in self.invalid:
            return
        url_name = resolve(path_info).url_name
        if url_name is None:
            return
        context = dict()
        self.kwargs = resolve(path_info).kwargs
        username = self.get_var("username")
        if username:
            self.user_obj = get_object_or_404(User, username=username)
            user_address = get_object_or_404(UserProfile, user=self.user_obj).address
            try:
                twitter_username = user_address.filter(choices="twitter")[0].address
            except IndexError:
                twitter_username = ""
            else:
                context["twitter_username"] = twitter_username
            try:
                facebook_username = user_address.filter(choices="facebook")[0].address
            except IndexError:
                facebook_username = ""
            else:
                context["facebook_username"] = facebook_username
        make_f_name = url_name.replace("-", "_")
        try:
            for key, value in getattr(self, make_f_name).items():
                context[key] = value
            request.meta = context
        except AttributeError:
            context["title"] = make_f_name
            context["keywords"] = url_name
            context["description"] = url_name
            context["image"] = self.default_img
            request.meta = context

    def get_var(self, name):
        return self.kwargs.get(name)


class HeadMiddleware(MiddlewareMixin, HeadMixin):
    @property
    def content_detail(self):
        content = get_object_or_404(
            Content, user=self.user_obj, permlink=self.get_var("permlink")
        )
        keywords = ""
        for key in content.tags.split():
            keywords += key + ", "
        return dict(
            title=f"{content.utopic.name.capitalize()} | {content.title.capitalize()}",
            keywords=f"{keywords}{content.utopic.name.lower()}",
            description=content.description.capitalize(),
            image=content.utopic.image_address
            or content.image_address
            or self.default_img,
        )

    @property
    def embed(self):
        return self.content_detail

    @property
    def topic(self):
        topic = get_object_or_404(Topic, permlink=self.get_var("permlink"))
        try:
            description = topic.description.capitalize()
        except AttributeError:
            description = topic.name
        return dict(
            title=f"{topic.name} - Topic | Coogger".capitalize(),
            keywords=topic.name,
            description=description,
            image=topic.image_address or self.default_img,
        )

    @property
    def comment(self):
        username = self.get_var("username")
        return dict(
            title=f"{username} - comment".capitalize(),
            keywords=f"{username}, comment {username}, comment",
            description=f"comment {username}".capitalize(),
            image=self.default_img,
        )

    @property
    def language(self):
        language = self.get_var("language")
        return dict(
            title=f"{language} language | coogger".capitalize(),
            keywords=f"{language}, language {language}",
            description=f"Latest post on coogger from {language} language".capitalize(),
            image=self.default_language_img,
        )

    @property
    def user(self):
        username = self.get_var("username")
        return dict(
            title=f"{username} • coogger".capitalize(),
            keywords=f"{username}, coogger {username}",
            description=f"The latest posts from {username} on coogger".capitalize(),
            image=self.user_obj.githubauthuser.avatar_url or self.default_img,
        )

    @property
    def userabout(self):
        username = self.get_var("username")
        return dict(
            title=f"{username} | About".capitalize(),
            keywords=f"about {username}, {username}, about",
            description=f"About of {username}".capitalize(),
            image=self.user_obj.githubauthuser.avatar_url or self.default_img,
        )

    @property
    def detail_utopic(self):
        permlink = self.get_var("permlink")
        username = self.get_var("username")
        utopic = UTopic.objects.filter(user=self.user_obj, permlink=permlink)[0]
        if utopic.description:
            description = f"{utopic.description.capitalize()} | {username}"
        else:
            description = f"{username}'s contents about topic of {utopic}"
        return dict(
            title=f"{utopic} - Topic | {username}".capitalize(),
            keywords=utopic,
            description=description,
            image=utopic.image_address or self.user_obj.githubauthuser.avatar_url,
        )

    @property
    def settings(self):
        return dict(
            title="settings",
            keywords="settings,coogger settings",
            description="Coogger settings,",
            image=self.default_img,
        )

    @property
    def hashtag(self):
        tag = self.get_var("tag")
        return dict(
            title=f"coogger lates post from '{tag}' hashtag.",
            keywords=f"{tag}",
            description=f"coogger lates post from '{tag}' hashtag.",
            image=self.default_hashtag_img,
        )

    @property
    def explorer_posts(self):
        return dict(
            title=f"coogger",
            keywords=f"coogger, developers, experience, documentation, blogs, projects, publish",
            description="""Coogger is a platform for developers to publish their knowledge, experiences, documents or blogs in the best way.""",
            image=self.default_img,
        )

    @property
    def index(self):
        return self.explorer_posts

    @property
    def issues(self):
        username = self.get_var("username")
        utopic_permlink = self.get_var("utopic_permlink")
        title = f"{username}/{utopic_permlink} | issues".capitalize()
        utopic = UTopic.objects.filter(user=self.user_obj, permlink=utopic_permlink)[0]
        return dict(
            title=title,
            keywords=f"{utopic_permlink}, {username}",
            description=title,
            image=utopic.image_address or self.user_obj.githubauthuser.avatar_url,
        )

    @property
    def detail_issue(self):
        utopic_permlink = self.get_var("utopic_permlink")
        username = self.get_var("username")
        permlink = self.get_var("permlink")
        title = f"{username}/{utopic_permlink} - {permlink} | issue".capitalize()
        utopic = UTopic.objects.filter(user=self.user_obj, permlink=utopic_permlink)[0]
        return dict(
            title=title,
            keywords=f"{utopic_permlink}, {username}",
            description=title,
            image=utopic.image_address or self.user_obj.githubauthuser.avatar_url,
        )

    @property
    def commits(self):
        topic_permlink = self.get_var("topic_permlink")
        username = self.get_var("username")
        title = f"{username}/{topic_permlink} | commits".capitalize()
        utopic = UTopic.objects.filter(user=self.user_obj, permlink=topic_permlink)[0]
        return dict(
            title=title,
            keywords=f"{topic_permlink}, {username}",
            description=title,
            image=utopic.image_address or self.user_obj.githubauthuser.avatar_url,
        )

    @property
    def commit(self):
        hash = self.get_var("hash")
        topic_permlink = self.get_var("topic_permlink")
        username = self.get_var("username")
        commit = get_object_or_404(Commit, hash=hash)
        title = f"{username}/{topic_permlink} - {commit.msg} | commit".capitalize()
        return dict(
            title=title,
            keywords=f"{topic_permlink}, {username}, {commit.msg}, commit",
            description=title,
            image=commit.utopic.image_address
            or self.user_obj.githubauthuser.avatar_url,
        )

    @property
    def feed(self):
        username = self.get_var("username")
        title = f"{username}'s Feed".capitalize()
        return dict(
            title=title,
            keywords=f"{username}, feed",
            description=title,
            image=self.user_obj.githubauthuser.avatar_url or self.default_img,
        )

    @property
    def reply_detail(self):
        username = self.get_var("username")
        permlink = self.get_var("permlink")
        reply = ThreadedComments.objects.get(user__username=username, permlink=permlink)
        return dict(
            title=f"{reply.body[: 55]} | reply",
            keywords=reply.body[:55].replace(" ", ", "),
            description=f"{reply.body[: 55]}",
            image=self.user_obj.githubauthuser.avatar_url,
        )
