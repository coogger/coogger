from django.contrib.admin import ModelAdmin,StackedInline,site,TabularInline,AdminSite
from django.utils import timezone
from django.contrib import messages as ms
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.conf import settings

#models
from cooggerapp.models import *

# python
import datetime

# sc2py.
from sc2py.sc2py import Sc2
from sc2py.operations import Operations
from sc2py.operations import Vote

from easysteem.easysteem import Oogg
Oogg = Oogg(settings.STEEM)

#steem
from steem.post import Post

class ContentAdmin(ModelAdmin):
    list_ = ["user","content_list","title","permlink","tag","cooggerup","status","time","mod","modcomment"]
    list_display = list_
    list_display_links = list_
    list_filter = ["status","time","cooggerup","approved","cantapproved"]
    search_fields = ["content_list","title","permlink","tag"]
    fields = ("user","content_list","title","content","tag",("approved","cantapproved","upvote"),"status")

    def save_model(self, request, obj, form, change):
        obj.lastmod = datetime.datetime.now()
        request_user = str(request.user)
        oiouof = OtherInformationOfUsers.objects.filter(user = request.POST["user"])
        post = Post(post = obj.get_absolute_url())
        obj.mod = request.user #içerik ile ilgilenen mod
        if not obj.cooggerup: # bot oy atmadı ise daha aşağıdakilerin çalışmasına gerek yok,bu son işlem çünkü
            if obj.upvote == True and obj.status == "approved": # upvote with cooggerup
                for up in OtherInformationOfUsers.objects.filter(cooggerup_confirmation = True):
                    user, access_token, percent = up.user, up.s_info()["access_token"], up.cooggerup_percent
                    vote_json = Vote(voter = user, author = obj.user, permlink = obj.permlink, weight = int(percent)).json
                    data = Operations(vote_json).json
                    Sc2(token = access_token,data = data).run
                obj.cooggerup = True
            if obj.status == "approved":
                if obj.modcomment == False:
                    Oogg.reply(
                    title = "coogger | your contribution has been approved",
                    body = settings.APPROVED.format(obj.approved.replace("-"," ")),
                    author = request_user,
                    identifier = str(post.identifier)
                    )
                    obj.modcomment = True
            elif obj.status == "rejected":
                if obj.modcomment == False:
                    Oogg.reply(
                    title = "coogger | your contribution cannot be approved",
                    body = settings.CAN_NOT_BE_APPROVED.format(obj.cantapproved.replace("-"," ")),
                    author = request_user,
                    identifier = str(post.identifier)
                    )
                    obj.modcomment = True
        content_count = Content.objects.filter(user = obj.user,status = "approved").count()
        oiouof.update(hmanycontent = content_count)
        super(ContentAdmin, self).save_model(request, obj, form, change)

class UserFollowAdmin(ModelAdmin):
    list_ = ["user","choices","adress"]
    list_display = list_
    list_display_links = list_
    list_filter = ["choices"]
    search_fields = list_

class SearchedWordsAdmin(ModelAdmin):
    list_ = ["word","hmany"]
    list_display = list_
    list_display_links = list_
    search_fields = list_

class ContentviewsAdmin(ModelAdmin):
    list_ = ["content_id","ip"]
    list_display = list_
    list_display_links = list_
    search_fields = list_

class OtherInfoUsersAdmin(ModelAdmin):
    list_ = ["user","follower_count","following_count","hmanycontent","cooggerup_confirmation","cooggerup_percent"]
    list_display = list_
    list_display_links = list_
    search_fields = list_
    list_filter = ["cooggerup_confirmation"]

## users ##
class OtherInformationOfUsersAdmin(StackedInline):
    model = OtherInformationOfUsers
    can_delete = False
    verbose_name_plural = 'kullanıcıların diğer bilgileri'

class UserAdmin(UserAdmin):
    inlines = (OtherInformationOfUsersAdmin, )

site.unregister(User)
site.register(User, UserAdmin)
site.register(Content,ContentAdmin)
site.register(Contentviews,ContentviewsAdmin)
site.register(UserFollow,UserFollowAdmin)
site.register(SearchedWords,SearchedWordsAdmin)
site.register(ReportModel)
site.register(OtherInformationOfUsers,OtherInfoUsersAdmin)
