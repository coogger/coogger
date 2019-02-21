from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve
from django.contrib.auth import authenticate

# models
from core.cooggerapp.models import Content, Topic
from django.contrib.auth.models import User

from bs4 import BeautifulSoup
import mistune


class HeadMiddleware(MiddlewareMixin):

    def process_request(self, request):
        self.path_info = request.path_info
        invalid = ["sitemap", "api", "robots.txt"]
        if self.path_info.split("/")[1] in invalid:
            return None
        url_name = resolve(self.path_info).url_name
        self.kwargs = resolve(self.path_info).kwargs
        request.head = eval(f"self.{url_name}()")

    def detail(self):
        username = self.kwargs.get("username")
        permlink = self.kwargs.get("permlink")
        user = authenticate(username=username)
        try:
            content = Content.objects.filter(user=user, permlink=permlink)[0]
        except IndexError:
            # there isn't on coogger
            return dict(title="", keywords="", description="", image="")
        else:
            keywords = ""
            for key in content.tags.split():
                keywords += key+", "
            return dict(
                title=f"{content.topic.name.capitalize()} | {content.title.capitalize()}",
                keywords=f"{keywords}{content.topic.name.lower()}",
                description=self.get_soup(content.body).text[0:200].replace("\n"," ").capitalize(),
                image=self.get_image(content),
            )

    def topic(self):
        topic = Topic.objects.filter(name=self.kwargs.get("topic"))[0]
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
            title=f"Latest post on coogger from {cat_name} category".capitalize(),
            keywords=f"{cat_name}, {cat_name} category",
            description=f"Latest post on coogger from {cat_name} category".capitalize(),
            image="/static/media/topics/category.svg",
        )

    def language(self):
        lang_name = self.kwargs.get("lang_name")
        return dict(
            title=f"{lang_name} language | coogger".capitalize(),
            keywords=f"{lang_name}, language {lang_name}",
            description=f"Latest post on coogger from {lang_name} language".capitalize(),
            image="/static/media/topics/language.svg",
        )

    def user(self):
        username = self.kwargs.get("username")
        return dict(
            title=f"{username} • coogger knowledge content".capitalize(),
            keywords=f"{username}, coogger {username}",
            description=f"The latest posts from {username} on coogger".capitalize(),
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

    def review(self):
        return dict(
            title=f"latest posts pending approval on coogger",
            keywords=f"review,coogger review,approval",
            description=f"latest posts pending approval on coogger",
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
            title=f"coogger lates post from '{tag}' hashtag.",
            keywords=f"{tag}",
            description=f"coogger lates post from '{tag}' hashtag.",
            image="/static/media/icons/list.svg",
        )

    def home(self):
        return dict(
            title=f"coogger",
            keywords=f"coogger",
            description="Coogger is an ecosystem where is knowledge sharing network",
            image="https://www.coogger.com/static/logos/png/800.png",
        )

    @staticmethod
    def get_soup(text):
        renderer = mistune.Renderer(escape=False, parse_block_html=True)
        markdown = mistune.Markdown(renderer=renderer)
        return BeautifulSoup(markdown(text), "html.parser")

    def get_image(self, content):
        steemitimages = "https://steemitimages.com/0x0/"
        coogger_icon_image = f"{steemitimages}https://cdn.steemitimages.com/DQmV7q45hYaS1TugkYDmR4NtUuLXjMGDEnN2roxGGXJeYgs"
        try:
            return steemitimages+self.get_soup(content.body).find('img').get('src')
        except:
            return coogger_icon_image
