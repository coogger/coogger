from django.contrib.admin import ModelAdmin,StackedInline,site,TabularInline,AdminSite
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.conf import settings

#models
from apps.cooggerapp.models import *

# python
import datetime

# sc2py
from sc2py.sc2py import Sc2
from easysteem.easysteem import Oogg
Oogg = Oogg(settings.STEEM)

#steem
from steem.post import Post

class ContentAdmin(ModelAdmin):
    list_ = ["user","content_list","title","upvote"]
    list_display = list_
    list_display_links = list_
    list_filter = ["time","confirmation","upvote"]
    search_fields = list_
    fields = ("user","permlink",("content_list"),("title"),"content","show","tag",("views","hmanycomment","dor"),("confirmation","draft","cooggerup","upvote"))

    def save_model(self, request, obj, form, change):
        obj.lastmod = datetime.datetime.now()
        oiouof = OtherInformationOfUsers.objects.filter(user = request.POST["user"])
        if obj.cooggerup == True and obj.upvote == False:
            for up in OtherInformationOfUsers.objects.filter(cooggerup_confirmation = True):
                user, access_token, percent = up.user, up.s_info()["access_token"], up.cooggerup_percent
                Sc2(access_token).vote(voter = user, author = obj.user, permlink = obj.get_steemit_permlink(), weight = int(percent))
            post = Post(post = obj.get_steemit_url())
            if "coogger" not in Oogg.get_replies_list(post):
                Oogg.reply(title = "coogger | your contribution has been approved",body = settings.COOGGERUP_REPLY, author = "coogger", identifier = post.identifier)
            obj.upvote = True
        content_count = Content.objects.filter(user = obj.user).count()
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
