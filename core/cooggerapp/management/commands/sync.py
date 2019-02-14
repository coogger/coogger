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
        payload = steemconnect_user.filter()
        for sc_user in steemconnect_user.get(payload):
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

    def user(self):
        user_filter_api = UserFilterApi(data=self.data)
        payload = user_filter_api.filter()
        for user in user_filter_api.get(payload):
            self.user_update(user.username)

    def user_update(self, username):
        user = authenticate(username=username)
        try:
            user_api = UserApi(
                username=username,
                data=self.data
            ).ditop
        except Exception as e:
            print(e, username)
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
        all_contents = []
        content_filter_api = ContentFilterApi(data=self.data)
        payload = content_filter_api.filter(dapp="coogger", status="approved")
        for content in content_filter_api.get(payload):
            all_contents.append(content)
        return reversed(all_contents)

    def content(self):
        for post in self.get_all_contents():
            user = self.user_update(username=post.username)
            c_object = Content.objects.filter(user=user, permlink=post.permlink)
            if not c_object.exists():
                try:
                    mod = self.user_update(post.modusername)
                except AttributeError:
                    mod = None
                category_id = Category.objects.filter(name=post.category)
                if not category_id.exists():
                    Category(name=post.category).save()
                    category_id = Category.objects.filter(name=post.category)
                Content(
                    user=user,
                    title=post.title,
                    permlink=post.permlink,
                    body=post.content,
                    tags=post.tags,
                    language=post.language,
                    category=category_id[0],
                    definition=post.definition,
                    topic=self.topic(post.topic),
                    status=post.status,
                    views=post.views,
                    created=post.created,
                    last_update=post.last_update,
                    mod=mod,
                    cooggerup=post.cooggerup,
                ).save()
                utopic = UTopic.objects.filter(user=user, name=post.topic)
                if utopic.exists():
                    utopic.update(address=post.address)
                else:
                    UTopic(user=user, name=post.topic, address=post.address).save()
                    utopic = UTopic.objects.filter(user=user, name=post.topic)
                content = Content.objects.filter(user=user, permlink=post.permlink)[0]
                if not Commit.objects.filter(utopic=utopic[0], content=content).exists():
                    Commit(
                        user=user,
                        utopic=utopic[0],
                        content=content,
                        body=content.body,
                        msg=f"{post.title} Published."
                        ).save()
            self.views(id=post.id, obj=c_object)

    def searched(self):
        search_filter_api = SearchFilterApi(data=self.data)
        payload = search_filter_api.filter()
        for searched in search_filter_api.get(payload):
            word = searched.word
            s_object = SearchedWords.objects.filter(word=word)
            if s_object.exists():
                s_object.update(hmany=searched.hmany)
            else:
                SearchedWords(
                    word=word,
                    hmany=searched.hmany,
                ).save()

    def useraddresses(self):
        filter_user_address = UserAddresFilterApi(data=self.data)
        payload = filter_user_address.filter()
        for searched in filter_user_address.get(payload):
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

    def views(self, id, obj):
        filter_views = ViewsFilterApi(data=self.data)
        payload = filter_views.filter(content=id)
        count = filter_views.count(payload)
        print(f"{obj} views >> {count}")
        view_obj = Contentviews.objects.filter(content_id=obj[0].id)
        if view_obj.exists():
            if count == view_obj.count():
                return
        for view in filter_views.get(payload):
            if not view_obj.filter(ip=view.ip).exists():
                Contentviews(content_id=obj[0].id, ip=view.ip).save()

    def topic(self, name):
        topic_views = TopicFilterApi(data=self.data)
        payload = topic_views.filter(name=name)
        if topic_views.count(payload) == 0:
            try:
                Topic.objects.filter(name=name)[0]
            except IndexError:
                Topic(name=name).save()
                return Topic.objects.filter(name=name)[0]
        else:
            for topic in topic_views.get(payload):
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
                return t_obj[0]


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
