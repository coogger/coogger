from django.contrib.auth.models import User
from django.urls import resolve
from django.utils.deprecation import MiddlewareMixin

from ..models import Commit, Content, Topic, UserProfile, UTopic


class HeadMixin:
    def process_request(self, request):
        path_info = request.path_info
        invalid = ["sitemap", "api", "robots.txt"]
        if path_info.split("/")[1] in invalid:
            return None
        url_name = resolve(path_info).url_name
        if url_name is None:
            return None
        self.context = dict()
        kwargs = resolve(path_info).kwargs
        # images
        self.default_img = "https://www.coogger.com/static/logos/png/800.png"
        self.default_hashtag_img = "/static/media/icons/list.svg"
        self.default_category_img = "/static/media/topics/category.svg"
        self.default_language_img = "/static/media/topics/language.svg"
        # all variable in kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)
        if hasattr(self, "username"):
            self.user_obj = User.objects.get(username=self.username)
            user_address = UserProfile.objects.get(user=self.user_obj).address
            try:
                self.twitter_author = user_address.filter(choices="twitter")[0].address
            except IndexError:
                self.twitter_author = ""
            else:
                self.context["twitter_author"] = self.twitter_author
            try:
                self.facebook_author = user_address.filter(choices="facebook")[
                    0
                ].address
            except IndexError:
                self.facebook_author = ""
            else:
                self.context["facebook_author"] = self.facebook_author
        try:
            for key, value in getattr(self, url_name.replace("-", "_"))().items():
                self.context[key] = value
            request.head = self.context
        except AttributeError:
            request.head = dict(
                title=url_name.title(),
                keywords=url_name,
                description=url_name,
                image=self.default_img,
            )


class HeadMiddleware(MiddlewareMixin, HeadMixin):
    def content_detail(self):
        content = Content.objects.get(user=self.user_obj, permlink=self.permlink)
        keywords = ""
        for key in content.tags.split():
            keywords += key + ", "
        return dict(
            title=f"{content.utopic.name.capitalize()} | {content.title.capitalize()}",
            keywords=f"{keywords}{content.utopic.name.lower()}",
            description=content.description.capitalize(),
            image=content.image_address or self.default_img,
        )

    def embed(self):
        return self.content_detail()

    def topic(self):
        topic = Topic.objects.get(permlink=self.permlink)
        try:
            description = topic.definition.capitalize()
        except AttributeError:
            description = topic.name
        return dict(
            title=f"{topic.name} - Topic | Coogger".capitalize(),
            keywords=topic.name,
            description=description,
            image=topic.image_address or self.default_img,
        )

    def comment(self):
        return dict(
            title=f"{self.username} - comment".capitalize(),
            keywords=f"{self.username}, comment {self.username}, comment",
            description=f"comment {self.username}".capitalize(),
            image=self.default_img,
        )

    def category(self):
        return dict(
            title=f"Latest post on coogger from {self.cat_name} category".capitalize(),
            keywords=f"{self.cat_name}, {self.cat_name} category",
            description=f"Latest post on coogger from {self.cat_name} category".capitalize(),
            image=self.default_category_img,
        )

    def language(self):
        return dict(
            title=f"{self.lang_name} language | coogger".capitalize(),
            keywords=f"{self.lang_name}, language {self.lang_name}",
            description=f"Latest post on coogger from {self.lang_name} language".capitalize(),
            image=self.default_language_img,
        )

    def user(self):
        return dict(
            title=f"{self.username} • coogger".capitalize(),
            keywords=f"{self.username}, coogger {self.username}",
            description=f"The latest posts from {self.username} on coogger".capitalize(),
            image=self.user_obj.githubauthuser.avatar_url or self.default_img,
        )

    def userabout(self):
        return dict(
            title=f"{self.username} | About".capitalize(),
            keywords=f"about {self.username}, {self.username}, about",
            description=f"About of {self.username}".capitalize(),
            image=self.user_obj.githubauthuser.avatar_url or self.default_img,
        )

    def detail_utopic(self):
        utopic = UTopic.objects.filter(user=self.user_obj, permlink=self.permlink)[0]
        if utopic.definition:
            definition = f"{utopic.definition.capitalize()} | {self.username}"
        else:
            definition = f"{self.username}'s contents about topic of {utopic}"
        if utopic.image_address:
            image = utopic.image_address
        else:
            image = self.user_obj.githubauthuser.avatar_url
        return dict(
            title=f"{utopic} - Topic | {self.username}".capitalize(),
            keywords=utopic,
            description=definition,
            image=image or self.default_img,
        )

    def settings(self):
        return dict(
            title="settings",
            keywords="settings,coogger settings",
            description="Coogger settings,",
            image=self.default_img,
        )

    def hashtag(self):
        return dict(
            title=f"coogger lates post from '{self.tag}' hashtag.",
            keywords=f"{self.tag}",
            description=f"coogger lates post from '{self.tag}' hashtag.",
            image=self.default_hashtag_img,
        )

    def explorer_posts(self):
        return dict(
            title=f"coogger",
            keywords=f"coogger, developers, experience, documentation, blogs, projects",
            description="""
                Coogger is a platform where developers can write their knowledge,
                experience, documentation and blogs about their projects or projects which love.""",
            image=self.default_img,
        )

    def home(self):
        return self.explorer_posts()

    def issues(self):
        title = f"{self.utopic_permlink}/{self.username} | issues".capitalize()
        return dict(
            title=title,
            keywords=f"{self.utopic_permlink}, {self.username}",
            description=title,
            image=self.user_obj.githubauthuser.avatar_url or self.default_img,
        )

    def detail_issue(self):
        title = f"{self.utopic_permlink}/{self.username} - {self.permlink} | issue".capitalize()
        return dict(
            title=title,
            keywords=f"{self.utopic_permlink}, {self.username}",
            description=title,
            image=self.user_obj.githubauthuser.avatar_url or self.default_img,
        )

    def commits(self):
        title = f"{self.topic_permlink}/{self.username} | commits".capitalize()
        return dict(
            title=title,
            keywords=f"{self.topic_permlink}, {self.username}",
            description=title,
            image=self.user_obj.githubauthuser.avatar_url or self.default_img,
        )

    def commit(self):
        commit = Commit.objects.get(hash=self.hash)
        title = f"{self.topic_permlink}/{self.username} - {commit.msg} | commit".capitalize()
        return dict(
            title=title,
            keywords=f"{self.topic_permlink}, {self.username}, {commit.msg}, commit",
            description=title,
            image=self.user_obj.githubauthuser.avatar_url or self.default_img,
        )

    def feed(self):
        title = f"{self.username}'s Feed".capitalize()
        return dict(
            title=title,
            keywords=f"{self.username}, feed",
            description=title,
            image=self.user_obj.githubauthuser.avatar_url or self.default_img,
        )
