# django
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# coogger-python
from coogger.content import ContentFilterApi
from coogger.user import SteemConnectUserApi, UserApi, UserFilterApi, SteemConnectFilterApi
from coogger.search import SearchFilterApi
from coogger.useraddress import UserAddresFilterApi
from coogger.views import ViewsFilterApi
from coogger.topic import TopicFilterApi

# core.*models
from core.cooggerapp.models import (OtherInformationOfUsers, Content,
    OtherAddressesOfUsers, SearchedWords,
    Contentviews, Topic, UTopic, Category, Commit)
from steemconnect_auth.models import SteemConnectUser


class Sync():

    def __init__(self, data):
        self.data = data

    def steemconnect_user(self):
        steemconnect_user = SteemConnectFilterApi(data=self.data)
        while True:
            steemconnect_user.filter()
            for sc_user in steemconnect_user.results:
                user = authenticate(username=sc_user.username)
                sc_object = SteemConnectUser.objects.filter(user=user)
                if sc_object.exists():
                    sc_object.update(
                        refresh_token=sc_user.refresh_token,
                        code=sc_user.code,
                        access_token=sc_user.access_token
                    )
                else:
                    SteemConnectUser(
                        user=user,
                        refresh_token=sc_user.refresh_token,
                        code=sc_user.code,
                        access_token=sc_user.access_token
                    ).save()
            if steemconnect_user.next:
                steemconnect_user.api_url = steemconnect_user.next
            else:
                break

    def user(self):
        user_filter_api = UserFilterApi(data=self.data)
        while True:
            user_filter_api.filter()
            for user in user_filter_api.results:
                self.user_update(user.username)
            if user_filter_api.next:
                user_filter_api.api_url = user_filter_api.next
            else:
                break

    def user_update(self, username):
        user = authenticate(username=username)
        try:
            user_api = UserApi(
                username=username,
                data=self.data
            ).ditop
        except Exception as e:
            print(e, username, "\r")
        else:
            oiou_object = OtherInformationOfUsers.objects.filter(user=user)
            if oiou_object.exists():
                oiou_object.update(
                    about=user_api.about,
                    cooggerup_confirmation=user_api.cooggerup_confirmation,
                    cooggerup_percent=user_api.cooggerup_percent,
                    vote_percent=user_api.vote_percent,
                    beneficiaries=user_api.beneficiaries,
                    sponsor=user_api.sponsor,
                    total_votes=user_api.total_votes,
                    total_vote_value=user_api.total_vote_value,
                    access_token=user_api.access_token,
                )
            else:
                OtherInformationOfUsers(
                    user=user,
                    about=user_api.about,
                    cooggerup_confirmation=user_api.cooggerup_confirmation,
                    cooggerup_percent=user_api.cooggerup_percent,
                    vote_percent=user_api.vote_percent,
                    beneficiaries=user_api.beneficiaries,
                    sponsor=user_api.sponsor,
                    total_votes=user_api.total_votes,
                    total_vote_value=user_api.total_vote_value,
                ).save()
        return user

    def get_all_contents(self):
        # TODO: there is a problem, it is not fetch all of content.
        content_filter_api = ContentFilterApi(data=self.data)
        all_contents = []
        while True:
            content_filter_api.filter(dapp="coogger")
            print(f"count >> {content_filter_api.ditop.count}, received >> {len(all_contents)}", "\r")
            for content in content_filter_api.results:
                all_contents.append(content)
            if content_filter_api.next:
                content_filter_api.api_url = content_filter_api.next
            else:
                break
        return reversed(all_contents)

    def content(self):
        for content in self.get_all_contents():
            user = self.user_update(content.username)
            topic = self.topic(content.topic)
            if topic is None:
                continue
            c_object = Content.objects.filter(user=user, permlink=content.permlink)
            if c_object.exists() and content.last_update != c_object[0].last_update:
                print(f"update a content >> {c_object}", "\r")
                try:
                    mod = User.objects.filter(username=content.modusername)[0]
                except AttributeError:
                    mod = None
                category_id = Category.objects.filter(name=content.category)
                c_object.update(
                    user=user,
                    title=content.title,
                    body=content.content,
                    tags=content.tags,
                    language=content.language,
                    category=category_id[0],
                    definition=content.definition,
                    topic=topic,
                    status=content.status,
                    views=content.views,
                    last_update=content.last_update,
                    mod=mod,
                    cooggerup=content.cooggerup,
                )
            else:
                print(f"saved a content -> {content.permlink}", "\r")
                try:
                    mod = User.objects.filter(username=content.modusername)[0]
                except AttributeError:
                    mod = None
                category_id = Category.objects.filter(name=content.category)
                if not category_id.exists():
                    Category(name=content.category).save()
                    category_id = Category.objects.filter(name=content.category)
                Content(
                    user=user,
                    title=content.title,
                    permlink=content.permlink,
                    body=content.content,
                    tags=content.tags,
                    language=content.language,
                    category=category_id[0],
                    definition=content.definition,
                    topic=topic,
                    status=content.status,
                    views=content.views,
                    created=content.created,
                    last_update=content.last_update,
                    mod=mod,
                    cooggerup=content.cooggerup,
                ).save()
                utopic = UTopic.objects.filter(user=user, name=content.topic)
                if utopic.exists():
                    utopic.update(address=content.address)
                else:
                    UTopic(user=user, name=content.topic, address=content.address).save()
                    utopic = UTopic.objects.filter(user=user, name=content.topic)
                content = Content.objects.filter(user=user, permlink=content.permlink)[0]
                if not Commit.objects.filter(utopic=utopic[0], content=content).exists():
                    Commit(utopic=utopic[0], content=content, body=content.body).save()

    def searched(self):
        search_filter_api = SearchFilterApi(data=self.data)
        while True:
            search_filter_api.filter()
            for searched in search_filter_api.results:
                word = searched.word
                s_object = SearchedWords.objects.filter(word=word)
                if s_object.exists():
                    s_object.update(hmany=searched.hmany)
                else:
                    SearchedWords(
                        word=word,
                        hmany=searched.hmany,
                    ).save()
            if search_filter_api.next:
                search_filter_api.api_url = search_filter_api.next
            else:
                break

    def useraddresses(self):
        filter_user_address = UserAddresFilterApi(data=self.data)
        while True:
            filter_user_address.filter()
            for searched in filter_user_address.results:
                user = self.user_update(searched.username)
                choices = searched.choices
                address = searched.address
                address_obj = OtherAddressesOfUsers.objects.filter(
                    user=user, choices=choices,
                    address=address
                    )
                if not address_obj.exists():
                    OtherAddressesOfUsers(
                        user=user,
                        choices=choices,
                        address=address,
                    ).save()
            if filter_user_address.next:
                filter_user_address.api_url = filter_user_address.next
            else:
                break

    def views(self):
        filter_views = ViewsFilterApi(data=self.data)
        content_filter_api = ContentFilterApi(data=self.data)
        while True:
            filter_views.filter()
            for view in filter_views.results:
                content_filter_api.filter(id=view.content, dapp="coogger")
                content = content_filter_api.results[0]
                try:
                    content = Content.objects.filter(user=self.user_update(content.username), permlink=content.permlink)[0]
                except IndexError:
                    pass
                else:
                    if not Contentviews.objects.filter(content=content, ip=view.ip).exists():
                        Contentviews(content=content, ip=view.ip).save()
            if filter_views.next:
                filter_views.api_url = filter_views.next
            else:
                break

    def topic(self, name):
        topic_views = TopicFilterApi(data=self.data)
        topic_views.filter(name=name)
        try:
            topic = topic_views.results[0]
        except Exception as e:
            Topic(name=name).save()
        else:
            t_obj = Topic.objects.filter(name=topic.name)
            if t_obj.exists():
                t_obj.update(
                    image_address=topic.image_address,
                    definition=topic.definition,
                    tags=topic.tags,
                    address=topic.address,
                    editable=topic.editable,
                    )
            else:
                print(f"create topic >> {topic.name}")
                Topic(
                    name=topic.name,
                    image_address=topic.image_address,
                    definition=topic.definition,
                    tags=topic.tags,
                    address=topic.address,
                    editable=topic.editable,
                    ).save()
            return Topic.objects.filter(name=topic.name)[0]


class Command(BaseCommand):
    help = "Sync to coogger.db from server to local"

    def add_arguments(self, parser):
        parser.add_argument("username", type=str)
        parser.add_argument("access_token", type=str)
        parser.add_argument("--which", type=str)

    def handle(self, *args, **kwargs):
        data = dict(
            username=kwargs.get("username"),
            access_token=kwargs.get("access_token")
        )
        which = kwargs.get("which")
        sync = Sync(data)
        if which is not None:
            eval(f"sync.{which}()")
        else:
            sync.steemconnect_user()
            sync.content()
            sync.useraddresses()
            sync.searched()
            # sync.user()
            # sync.views()
