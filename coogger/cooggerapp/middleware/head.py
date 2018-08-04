# her sayfa için geçerli bir head sayfası yapman için burayı hallet
from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve

# models
from cooggerapp.models import Content
from django.contrib.auth.models import User


from bs4 import BeautifulSoup
import mistune


class Head(object):
    def __init__(self, request):
        last_path = request.path_info.split("/")[-2]
        start_path = request.path_info.split("/")[1]
        url_name = resolve(request.path_info).url_name
        community_name = request.community_model.name
        if url_name == "category":
            setattr(self, "title", "Latest post on {} from {} category".format(community_name, last_path))
            setattr(self, "keywords", "{}, coogger categories,categories,category".format(last_path))
            setattr(self, "description", "Latest post on {} from {} category".format(community_name, last_path))
            # setattr(self, "face_author", "coogger {} category".format(last_path))
            setattr(self, "image", "/static/media/topics/category.svg")
        elif url_name == "language":
            setattr(self, "title", "Latest post on {} from {} language".format(community_name, last_path))
            setattr(self, "keywords", "{}, coogger languages,languages")
            setattr(self, "description", "Latest post on {} from {} language".format(community_name, last_path))
            # setattr(self, "face_author", "coogger {} category".format(last_path))
            setattr(self, "image", "/static/media/topics/language.svg")
        elif url_name == "user":
            setattr(self, "title", "The latest posts from {} on {}".format(last_path, community_name))
            setattr(self, "keywords", "{}, coogger {}".format(last_path, last_path))
            setattr(self, "description", "The latest posts from {} on {}".format(last_path, community_name))
            # setattr(self, "face_author", "coogger {} category".format(last_path))
            setattr(self, "image", "https://steemitimages.com/u/{}/avatar".format(last_path.replace("@", "")))
        elif url_name == "userabout":
            setattr(self, "title", "About of {}".format(last_path.replace("@", "")))
            setattr(self, "keywords", "about {},{}".format(last_path, last_path))
            setattr(self, "description", "About of {}".format(last_path.replace("@", "")))
            # setattr(self, "face_author", "coogger {} category".format(last_path))
            setattr(self, "image", "https://steemitimages.com/u/{}/avatar".format(last_path.replace("@", "")))
        elif url_name == "utopic":
            setattr(self, "title", "{}'s contents about topic of {}".format(last_path.replace("@", ""), start_path))
            setattr(self, "keywords", "{}, {}, coogger topic,topic".format(last_path.replace("@", ""), start_path))
            setattr(self, "description", "{}'s contents about topic of {}".format(last_path.replace("@", ""), start_path))
            # setattr(self, "face_author", "coogger {} category".format(last_path))
            setattr(self, "image", "https://steemitimages.com/u/{}/avatar".format(last_path.replace("@", "")))
        elif url_name == "followingcontent":
            setattr(self, "title", "feed")
            setattr(self, "keywords", "Coogger feed,feed")
            setattr(self, "description", "Coogger feed")
            # setattr(self, "face_author", "coogger {} category".format(last_path))
            # setattr(self, "image", "coogger {} category".format(last_path))
        elif url_name == "review":
            setattr(self, "title", "latest posts pending approval on {}".format(community_name))
            setattr(self, "keywords", "review,coogger review,approval".format(last_path))
            setattr(self, "description", "latest posts pending approval on {}".format(community_name))
            # setattr(self, "face_author", "coogger {} category".format(last_path))
            # setattr(self, "image", "coogger {} category".format(last_path))
        elif url_name == "settings":
            setattr(self, "title", "settings")
            setattr(self, "keywords", "settings,coogger settings")
            setattr(self, "description", "Coogger settings,")
            # setattr(self, "face_author", )
            # setattr(self, "image", "")
        elif url_name == "detail":
            user = User.objects.filter(username=start_path.replace("@", ""))[0]
            queryset = Content.objects.filter(user=user, permlink=last_path)[0]
            beautifultext = BeautifulSoup(queryset.definition, "html.parser")
            try:
               image = beautifultext.find("img").get("src")
            except:
                image = ""
            description = beautifultext.text[0:200]
            setattr(self, "title", queryset.title)
            setattr(self, "keywords", queryset.tag)
            setattr(self, "description", description)
            # setattr(self, "face_author", "coogger {} category".format(last_path))
            setattr(self, "image", image)
        elif url_name == "hashtag":
            setattr(self, "title", "{} lates post from '{}' hashtag.".format(community_name, last_path))
            setattr(self, "keywords", "{}, {} hashtag".format(last_path, community_name))
            setattr(self, "description", "{} lates post from '{}' hashtag.".format(community_name, last_path))
            # setattr(self, "face_author", "coogger {} category".format(last_path))
            setattr(self, "image", "/static/media/icons/list.svg")
        elif url_name == "home":
            renderer = mistune.Renderer(escape=False, parse_block_html=True)
            markdown = mistune.Markdown(renderer=renderer)
            beautifultext = BeautifulSoup(markdown(request.community_model.ms), "html.parser")
            try:
               image = beautifultext.find("img").get("src")
            except:
                image = ""
            description = beautifultext.text[0:200]
            setattr(self, "title", "{} | coogger".format(community_name))
            setattr(self, "keywords", "{}, coogger ecosystem,coogger/{}".format(community_name, community_name))
            setattr(self, "description", description)
            # setattr(self, "face_author", "coogger {} category".format(last_path))
            setattr(self, "image", image)


class HeadMiddleware(MiddlewareMixin):

    def process_request(self, request):
        request.head = Head(request)
