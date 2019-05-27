# django
from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve

# models
from core.cooggerapp.models import Content, Topic, UTopic
from django.contrib.auth.models import User

# python
from bs4 import BeautifulSoup
import mistune


class HeadMixin:

    def process_request(self, request):
        self.path_info = request.path_info
        invalid = ["sitemap", "api", "robots.txt"]
        if self.path_info.split("/")[1] in invalid:
            return None
        url_name = resolve(self.path_info).url_name
        if url_name is None:
            return None
        self.kwargs = resolve(self.path_info).kwargs
        try:
            request.head = getattr(self, url_name.replace("-", "_"))
        except AttributeError:
            request.head = dict(
                title=url_name.title(),
                keywords=url_name,
                description=url_name,
                image="")

    @staticmethod
    def get_soup(text):
        renderer = mistune.Renderer(escape=False, parse_block_html=True)
        markdown = mistune.Markdown(renderer=renderer)
        return BeautifulSoup(markdown(text), "html.parser")

    def get_image(self, content):
        coogger_icon_image = f"https://www.coogger.com/media/images/coogger_W56Ux33.png"
        try:
            return self.get_soup(content.body).find('img').get('src')
        except:
            return coogger_icon_image



class HeadMiddleware(MiddlewareMixin, HeadMixin):

    def detail(self):
        username = self.kwargs.get("username")
        permlink = self.kwargs.get("permlink")
        user = User.objects.get(username=username)
        content = Content.objects.filter(user=user, permlink=permlink)
        if not content.exists():
            return dict(title="", keywords="", description="", image="")
        content = content[0]
        keywords = ""
        for key in content.tags.split():
            keywords += key+", "
        return dict(
            title=f"{content.utopic.name.capitalize()} | {content.title.capitalize()}",
            keywords=f"{keywords}{content.utopic.name.lower()}",
            description=self.get_soup(content.body).text[0:200].replace("\n"," ").capitalize(),
            image=self.get_image(content),
        )

    def topic(self):
        topic = Topic.objects.filter(permlink=self.kwargs.get("permlink"))[0]
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
        permlink = self.kwargs.get("permlink")
        user = User.objects.get(username=username)
        utopic = UTopic.objects.filter(user=user, permlink=permlink)[0]
        if utopic.definition:
            definition = f"{utopic.definition.capitalize()} | {username}"
        else:
            definition = f"{username}'s contents about topic of {utopic}"
        if utopic.image_address:
            image = utopic.image_address
        else:
            image = f"https://steemitimages.com/u/{username}/avatar"
        return dict(
            title=f"{utopic} - Topic | {username}".capitalize(),
            keywords=utopic,
            description=definition,
            image=image,
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

