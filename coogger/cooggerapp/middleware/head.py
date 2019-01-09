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


class Head(object):
    def __init__(self, request):
        last_path = request.path_info.split("/")[-2]
        start_path = request.path_info.split("/")[1]
        url_name = resolve(request.path_info).url_name
        dapp_name = request.dapp_model.name
        if url_name == "category":
            setattr(self, "title", f"Latest post on {dapp_name} from {last_path} category")
            setattr(self, "keywords", f"{last_path}, coogger categories,categories,category")
            setattr(self, "description", f"Latest post on {dapp_name} from {last_path} category")
            setattr(self, "image", "/static/media/topics/category.svg")
        elif url_name == "language":
            setattr(self, "title", f"Latest post on {dapp_name} from {last_path} language")
            setattr(self, "keywords", "coogger languages,languages")
            setattr(self, "description", f"Latest post on {dapp_name} from {last_path} language")
            setattr(self, "image", "/static/media/topics/language.svg")
        elif url_name == "user":
            setattr(self, "title", f"The latest posts from {last_path} on {dapp_name}")
            setattr(self, "keywords", f"{last_path}, coogger {last_path}")
            setattr(self, "description", f"The latest posts from {last_path} on {dapp_name}")
            setattr(self, "image", "https://steemitimages.com/u/{}/avatar".format(last_path.replace("@", "")))
        elif url_name == "userabout":
            setattr(self, "title", "About of {}".format(last_path.replace("@", "")))
            setattr(self, "keywords", "about {},{}".format(last_path, last_path))
            setattr(self, "description", "About of {}".format(last_path.replace("@", "")))
            setattr(self, "image", "https://steemitimages.com/u/{}/avatar".format(last_path.replace("@", "")))
        elif url_name == "utopic":
            setattr(self, "title", "{}'s contents about topic of {}".format(last_path.replace("@", ""), start_path))
            setattr(self, "keywords", "{}, {}, coogger topic,topic".format(last_path.replace("@", ""), start_path))
            setattr(self, "description", "{}'s contents about topic of {}".format(last_path.replace("@", ""), start_path))
            setattr(self, "image", "https://steemitimages.com/u/{}/avatar".format(last_path.replace("@", "")))
        elif url_name == "followingcontent":
            setattr(self, "title", "feed")
            setattr(self, "keywords", "Coogger feed,feed")
            setattr(self, "description", "Coogger feed")
        elif url_name == "review":
            setattr(self, "title", "latest posts pending approval on {}".format(dapp_name))
            setattr(self, "keywords", "review,coogger review,approval".format(last_path))
            setattr(self, "description", "latest posts pending approval on {}".format(dapp_name))
        elif url_name == "settings":
            setattr(self, "title", "settings")
            setattr(self, "keywords", "settings,coogger settings")
            setattr(self, "description", "Coogger settings,")
        elif url_name == "detail":
            username = start_path.replace("@", "")
            user = authenticate(username=username)
            POST = Post(post=f"@{username}/{last_path}")
            title = POST.title
            keywords = ""
            for key in POST.tags:
                keywords += key+", "
            description = self.get_soup(POST.body).text[0:200].replace("\n"," ")
            setattr(self, "title", title)
            setattr(self, "keywords", keywords)
            setattr(self, "description", description)
            setattr(self, "image", self.get_image(POST))
        elif url_name == "hashtag":
            setattr(self, "title", "{} lates post from '{}' hashtag.".format(dapp_name, last_path))
            setattr(self, "keywords", "{}, {} hashtag".format(last_path, dapp_name))
            setattr(self, "description", "{} lates post from '{}' hashtag.".format(dapp_name, last_path))
            setattr(self, "image", "/static/media/icons/list.svg")
        elif url_name == "home":
            dapp = request.dapp_model
            if dapp.name == "coogger":
                setattr(self, "title", "{}".format(dapp.name))
            else:
                setattr(self, "title", "{} | coogger".format(dapp.name))
            setattr(self, "keywords", "{}, coogger ecosystem,coogger/{}".format(dapp.name, dapp.name))
            setattr(self, "description", dapp.definition)
            setattr(self, "author", f"https://www.facebook.com/{dapp.name}")
            setattr(self, "image", dapp.image)
        elif url_name == "topic":
            try:
                topic = Topic.objects.filter(name=last_path)[0]
            except IndexError:
                pass
            else:
                setattr(self, "title", f"Topic - {topic.name} | Coogger")
                setattr(self, "description", topic.definition)
                setattr(self, "image", topic.image_address)
    def get_soup(self, text):
        renderer = mistune.Renderer(escape=False, parse_block_html=True)
        markdown = mistune.Markdown(renderer=renderer)
        return BeautifulSoup(markdown(text), "html.parser")

    def get_image(self, POST):
        try:
            return f"https://steemitimages.com/0x0/{self.get_soup(POST.body).find('img').get('src')}"
        except:
            return "https://steemitimages.com/0x0/https://cdn.steemitimages.com/DQmV7q45hYaS1TugkYDmR4NtUuLXjMGDEnN2roxGGXJeYgs"


class HeadMiddleware(MiddlewareMixin):

    def process_request(self, request):
        request.head = Head(request)
