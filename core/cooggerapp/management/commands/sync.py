# django
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

# coogger-python
from coogger.content import ContentApi, ContentFilterApi
from coogger.user import SteemConnectUserApi, UserApi, UserFilterApi
from coogger.dapp import DappFilterApi, DappApi
from coogger.search import SearchFilterApi
from coogger.useraddress import UserAddresFilterApi
from coogger.views import ViewsFilterApi
from coogger.topic import TopicFilterApi

# core.*models
from core.cooggerapp.models import (OtherInformationOfUsers, Content,
    OtherAddressesOfUsers, SearchedWords, Contentviews, Topic
)
from core.steemconnect_auth.models import (
    Dapp, Mods, SteemConnectUser,
    DappSettings, CategoryofDapp)


class Sync(BaseCommand):

    def __init__(self, data):
        self.data = data
        super(Sync, self).__init__()

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
        get_user_from_db, created = User.objects.get_or_create(username=username)
        if created:
            self.stdout.write(f"created new user named >> {username}")
        try:
            user = UserApi(
                username=username,
                data=self.data
            ).ditop
        except Exception as e:
            self.stdout.write(e, username)
        else:
            oiou_object = OtherInformationOfUsers.objects.filter(user=get_user_from_db)
            if oiou_object.exists():
                oiou_object.update(
                    about=user.about,
                    cooggerup_confirmation=user.cooggerup_confirmation,
                    cooggerup_percent=user.cooggerup_percent,
                    vote_percent=user.vote_percent,
                    beneficiaries=user.beneficiaries,
                    sponsor=user.sponsor,
                    total_votes=user.total_votes,
                    total_vote_value=user.total_vote_value,
                    access_token=user.access_token,
                )
            else:
                OtherInformationOfUsers(
                    user=get_user_from_db,
                    about=user.about,
                    cooggerup_confirmation=user.cooggerup_confirmation,
                    cooggerup_percent=user.cooggerup_percent,
                    vote_percent=user.vote_percent,
                    beneficiaries=user.beneficiaries,
                    sponsor=user.sponsor,
                    total_votes=user.total_votes,
                    total_vote_value=user.total_vote_value,
                ).save()
        try:
            sc_user = SteemConnectUserApi(
                username=get_user_from_db.username,
                data=self.data
            ).ditop
        except Exception as e:
            self.stdout.write(e, username)
        else:
            sc_object = SteemConnectUser.objects.filter(user=get_user_from_db)
            if sc_object.exists():
                sc_object.update(
                    dapp=Dapp.objects.filter(id=sc_user.dapp)[0],
                    refresh_token=sc_user.refresh_token,
                    code=sc_user.code,
                    access_token=sc_user.access_token
                )
            else:
                SteemConnectUser(
                    user=get_user_from_db,
                    dapp=Dapp.objects.filter(id=sc_user.dapp)[0],
                    refresh_token=sc_user.refresh_token,
                    code=sc_user.code,
                    access_token=sc_user.access_token
                ).save()
        return get_user_from_db

    def get_all_contents(self):
        content_filter_api = ContentFilterApi(data=self.data)
        all_contents = []
        while True:
            content_filter_api.filter()
            self.stdout.write(f"count >> {content_filter_api.ditop.count}, received >> {len(all_contents)}")
            for content in content_filter_api.results:
                all_contents.append(content)
            if content_filter_api.next:
                content_filter_api.api_url = content_filter_api.next
            else:
                break
        return reversed(all_contents)

    def content(self):
        for content in self.get_all_contents():
            try:
                user = User.objects.filter(username=content.username)[0]
            except IndexError:
                self.user_update(content.username)
            c_object = Content.objects.filter(user=user, permlink=content.permlink)
            if c_object.exists():
                if content.last_update != c_object[0].last_update:
                    self.stdout.write(f"update a content >> {c_object}")
                    try:
                        mod = User.objects.filter(username=content.modusername)[0]
                    except AttributeError:
                        mod = None
                    c_object.update(
                        user=user,
                        dapp=Dapp.objects.filter(name=content.dapp_name)[0],
                        title=content.title,
                        content=content.content,
                        tags=content.tags,
                        language=content.language,
                        category=content.category,
                        definition=content.definition,
                        topic=content.topic,
                        status=content.status,
                        views=content.views,
                        last_update=content.last_update,
                        address=content.address,
                        mod=mod,
                        cooggerup=content.cooggerup,
                    )
            else:
                self.stdout.write(f"saved a content")
                try:
                    mod = User.objects.filter(username=content.modusername)[0]
                except AttributeError:
                    mod = None
                Content(
                    dapp=Dapp.objects.filter(name=content.dapp_name)[0],
                    user=user,
                    title=content.title,
                    permlink=content.permlink,
                    content=content.content,
                    tags=content.tags,
                    language=content.language,
                    category=content.category,
                    definition=content.definition,
                    topic=content.topic,
                    status=content.status,
                    views=content.views,
                    address=content.address,
                    created=content.created,
                    last_update=content.last_update,
                    mod=mod,
                    cooggerup=content.cooggerup,
                ).save()

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
                user = User.objects.filter(username=searched.username)[0]
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
        while True:
            filter_views.filter()
            for view in filter_views.results:
                content = Content.objects.filter(id=view.content)[0]
                if not Contentviews.objects.filter(content=content, ip=view.ip).exists():
                    Contentviews(content=content, ip=view.ip).save()
            if filter_views.next:
                filter_views.api_url = filter_views.next
            else:
                break

    def topic(self):
        topic_views = TopicFilterApi(data=self.data)
        while True:
            topic_views.filter()
            for top in topic_views.results:
                t_obj = Topic.objects.filter(name=top.name)
                if t_obj.exists():
                    t_obj.update(
                        image_address=top.image_address,
                        definition=top.definition,
                        tags=top.tags,
                        address=top.address,
                        editable=top.editable,
                        )
                else:
                    Topic(
                        name=top.name,
                        image_address=top.image_address,
                        definition=top.definition,
                        tags=top.tags,
                        address=top.address,
                        editable=top.editable,
                        ).save()
            if topic_views.next:
                topic_views.api_url = topic_views.next
            else:
                break


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
            sync.user()
            sync.dapp()
            sync.content()
            sync.useraddresses()
            sync.searched()
            sync.topic()
            sync.views()
