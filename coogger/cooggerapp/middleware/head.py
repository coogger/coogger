from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve
from django.contrib.auth import authenticate

# models
from cooggerapp.models import Content, Topic
from django.contrib.auth.models import User
from steemconnect_auth.models import CategoryofDapp

from bs4 import BeautifulSoup
import mistune

# steem
from steem.post import Post


class HeadMiddleware(MiddlewareMixin):

    def process_request(self, request):
        self.path_info = request.path_info
        invalid = ["sitemap", "api", "robots"]
        if self.path_info.split("/")[1] in invalid:
            return None
        url_name = resolve(self.path_info).url_name
        self.dapp_model = request.dapp_model
        self.last_path = self.path_info.split("/")[-2]
        self.start_path = self.path_info.split("/")[1]
        try:
            request.head = eval(f"self.{url_name}()")
        except AttributeError:
            pass

    def detail(self):
        username = self.start_path.replace("@", "")
        user = authenticate(username=username)
        post = Post(post=f"@{username}/{self.last_path}")
        keywords = ""
        for key in post.tags:
            keywords += key+", "
        return dict(
            title=post.title.capitalize(),
            keywords=keywords,
            description=self.get_soup(post.body).text[0:200].replace("\n"," ").capitalize(),
            image=self.get_image(post),
        )

    def topic(self):
        try:
            topic = Topic.objects.filter(name=self.last_path)[0]
        except IndexError:
            pass
        return dict(
            title=f"{topic.name} - Topic | Coogger".capitalize(),
            keywords=topic.name,
            description=topic.definition.capitalize(),
            image=topic.image_address,
        )

    def wallet(self):
        username = self.path_info.split("/")[2][1:]
        return dict(
            title=f"{username} - wallet".capitalize(),
            keywords=f"{username}, wallet {username}, wallet",
            description=f"Wallet {username}".capitalize(),
            image=None,
        )

    def activity(self):
        username = self.path_info.split("/")[2][1:]
        return dict(
            title=f"{username} - activity".capitalize(),
            keywords=f"{username}, activity {username}, activity",
            description=f"activity {username}".capitalize(),
            image=None,
        )

    def comment(self):
        username = self.path_info.split("/")[2][1:]
        return dict(
            title=f"{username} - comment".capitalize(),
            keywords=f"{username}, comment {username}, comment",
            description=f"comment {username}".capitalize(),
            image=None,
        )

    def category(self):
        return dict(
            title=f"Latest post on {self.dapp_model.name} from {self.last_path} category".capitalize(),
            keywords=f"{self.last_path}, {self.last_path} category",
            description=f"Latest post on {self.dapp_model.name} from {self.last_path} category".capitalize(),
            image="/static/media/topics/category.svg",
        )

    def language(self):
        return dict(
            title=f"{self.last_path} language | {self.dapp_model.name}".capitalize(),
            keywords=f"{self.last_path}, language {self.last_path}",
            description=f"Latest post on {self.dapp_model.name} from {self.last_path} language".capitalize(),
            image="/static/media/topics/language.svg",
        )

    def user(self):
        username = self.last_path[1:]
        return dict(
            title=f"{username} • {self.dapp_model.name} knowledge content".capitalize(),
            keywords=f"{self.last_path}, {username}, coogger {self.last_path}",
            description=f"The latest posts from {self.last_path} on {self.dapp_model.name}".capitalize(),
            image="https://steemitimages.com/u/{}/avatar".format(self.last_path.replace("@", "")),
        )

    def userabout(self):
        username = self.last_path[1:]
        return dict(
            title=f"{username} | About".capitalize(),
            keywords=f"about {username}, {username}, about",
            description=f"About of {username}".capitalize(),
            image=f"https://steemitimages.com/u/{username}/avatar",
        )

    def utopic(self):
        username = self.last_path[1:]
        return dict(
            title=f"{self.start_path} - {username}",
            keywords="{}, {}, coogger topic,topic".format(self.last_path.replace("@", ""), self.start_path),
            description="{}'s contents about topic of {}".format(self.last_path.replace("@", ""), self.start_path),
            image="https://steemitimages.com/u/{}/avatar".format(self.last_path.replace("@", "")),
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
            title="latest posts pending approval on {}".format(self.dapp_model.name),
            keywords="review,coogger review,approval".format(self.last_path),
            description="latest posts pending approval on {}".format(self.dapp_model.name),
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
        return dict(
            title="{} lates post from '{}' hashtag.".format(self.dapp_model.name, self.last_path),
            keywords="{}, {} hashtag".format(self.last_path, self.dapp_model.name),
            description="{} lates post from '{}' hashtag.".format(self.dapp_model.name, self.last_path),
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
