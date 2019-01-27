from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve
from django.contrib.auth import authenticate

# models
from core.cooggerapp.models import Content, Topic
from django.contrib.auth.models import User
from core.steemconnect_auth.models import CategoryofDapp

from bs4 import BeautifulSoup
import mistune

# steem
from steem.post import Post


class HeadMiddleware(MiddlewareMixin):

    def process_request(self, request):
        self.path_info = request.path_info
        invalid = ["sitemap", "api", "robots.txt"]
        if self.path_info.split("/")[1] in invalid:
            return None
        url_name = resolve(self.path_info).url_name
        self.kwargs = resolve(self.path_info).kwargs
        self.dapp_model = request.dapp_model
        try:
            request.head = eval(f"self.{url_name}()")
        except AttributeError:
            pass

    def detail(self):
        username = self.kwargs.get("username")
        permlink = self.kwargs.get("permlink")
        topic = self.kwargs.get("topic").capitalize()
        user = authenticate(username=username)
        post = Post(post=f"@{username}/{permlink}")
        keywords = ""
        for key in post.tags:
            keywords += key+", "
        return dict(
            title=f"{topic} | {post.title.capitalize()}",
            keywords=f"{keywords}{topic.lower()}",
            description=self.get_soup(post.body).text[0:200].replace("\n"," ").capitalize(),
            image=self.get_image(post),
        )

    def topic(self):
        try:
            topic = Topic.objects.filter(name=self.kwargs.get("topic"))[0]
        except IndexError:
            pass
        return dict(
            title=f"{topic.name} - Topic | Coogger".capitalize(),
            keywords=topic.name,
            description=topic.definition.capitalize(),
            image=topic.image_address,
        )

    def wallet(self):
        username = self.kwargs.get("username")
        return dict(
            title=f"{username} - wallet".capitalize(),
            keywords=f"{username}, wallet {username}, wallet",
            description=f"Wallet {username}".capitalize(),
            image=None,
        )

    def activity(self):
        username = self.kwargs.get("username")
        return dict(
            title=f"{username} - activity".capitalize(),
            keywords=f"{username}, activity {username}, activity",
            description=f"activity {username}".capitalize(),
            image=None,
        )

    def comment(self):
        username = self.kwargs.get("username")
        return dict(
            title=f"{username} - comment".capitalize(),
            keywords=f"{username}, comment {username}, comment",
            description=f"comment {username}".capitalize(),
            image=None,
        )

    def category(self):
        cat_name = self.kwargs.get("cat_name")
        return dict(
            title=f"Latest post on {self.dapp_model.name} from {cat_name} category".capitalize(),
            keywords=f"{cat_name}, {cat_name} category",
            description=f"Latest post on {self.dapp_model.name} from {cat_name} category".capitalize(),
            image="/static/media/topics/category.svg",
        )

    def language(self):
        lang_name = self.kwargs.get("lang_name")
        return dict(
            title=f"{lang_name} language | {self.dapp_model.name}".capitalize(),
            keywords=f"{lang_name}, language {lang_name}",
            description=f"Latest post on {self.dapp_model.name} from {lang_name} language".capitalize(),
            image="/static/media/topics/language.svg",
        )

    def user(self):
        username = self.kwargs.get("username")
        return dict(
            title=f"{username} • {self.dapp_model.name} knowledge content".capitalize(),
            keywords=f"{username}, coogger {username}",
            description=f"The latest posts from {username} on {self.dapp_model.name}".capitalize(),
            image=f"https://steemitimages.com/u/{username}/avatar",
        )

    def userabout(self):
        username = self.kwargs.get("username")
        return dict(
            title=f"{username} | About".capitalize(),
            keywords=f"about {username}, {username}, about",
            description=f"About of {username}".capitalize(),
            image=f"https://steemitimages.com/u/{username}/avatar",
        )

    def utopic(self):
        username = self.kwargs.get("username")
        topic = self.kwargs.get("topic")
        return dict(
            title=f"{topic} - {username}",
            keywords=f"{username}, {topic}",
            description=f"{username}'s contents about topic of {topic}",
            image=f"https://steemitimages.com/u/{username}/avatar",
        )

    def followingcontent(self):
        return dict(
            title="feed",
            keywords="Coogger feed,feed",
            description="Coogger feed",
            image=None,
        )

    def review(self):
        return dict(
            title=f"latest posts pending approval on {self.dapp_model.name}",
            keywords=f"review,coogger review,approval",
            description=f"latest posts pending approval on {self.dapp_model.name}",
            image=None,
        )

    def settings(self):
        return dict(
            title="settings",
            keywords="settings,coogger settings",
            description="Coogger settings,",
            image=None,
        )

    def hashtag(self):
        tag = self.self.kwargs.get("hashtag")
        return dict(
            title=f"{self.dapp_model.name} lates post from '{tag}' hashtag.",
            keywords=f"{tag}",
            description=f"{self.dapp_model.name} lates post from '{tag}' hashtag.",
            image="/static/media/icons/list.svg",
        )

    def home(self):
        return dict(
            title=f"{self.dapp_model.name}",
            keywords=f"{self.dapp_model.name}, coogger ecosystem,coogger/{self.dapp_model.name}",
            description=self.dapp_model.definition,
            image=self.dapp_model.image,
        )

    @staticmethod
    def get_soup(text):
        renderer = mistune.Renderer(escape=False, parse_block_html=True)
        markdown = mistune.Markdown(renderer=renderer)
        return BeautifulSoup(markdown(text), "html.parser")

    def get_image(self, post):
        steemitimages = "https://steemitimages.com/0x0/"
        coogger_icon_image = f"{steemitimages}https://cdn.steemitimages.com/DQmV7q45hYaS1TugkYDmR4NtUuLXjMGDEnN2roxGGXJeYgs"
        try:
            return steemitimages+self.get_soup(post.body).find('img').get('src')
        except:
            return coogger_icon_image
