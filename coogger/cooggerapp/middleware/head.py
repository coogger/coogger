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
        path_info = request.path_info
        split_path = path_info.split("/")
        url_name = resolve(path_info).url_name
        self.dapp_model = request.dapp_model
        self.last_path = split_path[-2]
        self.start_path = split_path[1]
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
            title=post.title,
            keywords=keywords,
            description=self.get_soup(post.body).text[0:200].replace("\n"," "),
            image=self.get_image(post),
        )

    def topic(self):
        try:
            topic = Topic.objects.filter(name=self.last_path)[0]
        except IndexError:
            pass
        return dict(
            title=f"Topic - {topic.name} | Coogger",
            keywords=topic.name,
            description=topic.definition,
            image=topic.image_address,
        )

    def category(self):
        return dict(
            title=f"Latest post on {self.dapp_model.name} from {self.last_path} category",
            keywords=f"{self.last_path}, coogger categories,categories,category",
            description=f"Latest post on {self.dapp_model.name} from {self.last_path} category",
            image="/static/media/topics/category.svg",
        )

    def language(self):
        return dict(
            title=f"Latest post on {self.dapp_model.name} from {self.last_path} language",
            keywords="coogger languages,languages",
            description=f"Latest post on {self.dapp_model.name} from {self.last_path} language",
            image="/static/media/topics/language.svg",
        )

    def user(self):
        return dict(
            title=f"The latest posts from {self.last_path} on {self.dapp_model.name}",
            keywords=f"{self.last_path}, coogger {self.last_path}",
            description=f"The latest posts from {self.last_path} on {self.dapp_model.name}",
            image="https://steemitimages.com/u/{}/avatar".format(self.last_path.replace("@", "")),
        )

    def userabout(self):
        return dict(
            title="About of {}".format(self.last_path.replace("@", "")),
            keywords="about {},{}".format(self.last_path, self.last_path),
            description="About of {}".format(self.last_path.replace("@", "")),
            image="https://steemitimages.com/u/{}/avatar".format(self.last_path.replace("@", "")),
        )

    def utopic(self):
        return dict(
            title="{}'s contents about topic of {}".format(self.last_path.replace("@", ""), self.start_path),
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
