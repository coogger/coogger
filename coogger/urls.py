from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

#views
from apps.views import AppsHome
from apps.views import AppsSitemap
from django.contrib.sitemaps.views import sitemap

# common addresses
urlpatterns = [
    url(r'^web/admin/', admin.site.urls), # admin panel
    url(r'^web/ckeditor/', include('ckeditor_uploader.urls')), # ckeditör
]

# main project = coogger
urlpatterns += [
    url(r"^",include("apps.cooggerapp.main_urls")), # home
    url(r'', include('social_django.urls'))
]

# apps mainpage
urlpatterns += [
    url(r'^apps/$',AppsHome.as_view(),name="apps-home"),
    url(r'^sitemap/apps\.xml/$', sitemap, {'sitemaps': {"apps":AppsSitemap()}}),
]

# other apps - her uygulama main_urls.py adında bir dosya açmalı ve adreslerini oraya koymalı - ordan başka yere yönlendirebilir.
for apps in settings.INSTALLED_APPS:
    if apps.startswith("apps."):
        app_name = apps.split(".")[1]
        if app_name != "cooggerapp":
            urlpatterns += [
                url(r"^apps/{}/".format(app_name),include("apps.{}.main_urls".format(app_name))),
            ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


# {"auth_time": 1521369788, "id": 644120, "expires": "604800",
# "granted_scopes":
#  ["vote", "comment", "comment_delete",
#  "comment_options", "custom_json", "claim_reward_balance"],
#  "account":
#  {"id": 644120, "name": "hakancelik", "owner":
#  {"weight_threshold": 1, "account_auths": [], "key_auths":
#  [["STM5ZhZGNu1gnuQr4gVrt8CmomxaeG7VdSeDN6YzNgf5j6kDDYc4j", 1]]},
#   "active": {"weight_threshold": 1, "account_auths": [], "key_auths":
#   [["STM4yBU8UetiGzzmGNReFUJofki6zBmjoaY79zKrhprPoAGBSoN6k", 1]]},
#   "posting": {"weight_threshold": 1, "account_auths": [["busy.app", 1],
#   ["coogger.app", 1], ["steem-plus-app", 1], ["steemplay.app", 1],
#   ["utopian.app", 1]], "key_auths":
#   [["STM6WqeJkXJGtMBR1Lc5zt1PyvkmoSpqESCxPE7VzynEdAacAnzuw", 1]]},
#   "memo_key": "STM8kD92xTrZyuhbJnMX4HM5X1Jdzn8naNV9M6Yy7SZs94rbJYm3a",
#    "json_metadata": {"profile": {"about": "Electrical and Electronics Engineer, founder of coogger.com / software developer",
#    "location": "Turkey", "website": "http://www.coogger.com",
#    "profile_image": "http://www.coogger.com/media/users/pp/pp-hakancelik.jpg",
#    "cover_image": "http://www.coogger.com/static/media/favicon.png",
#     "name": "Hakan \u00c7EL\u0130K"}}, "proxy": "",
#      "last_owner_update": "2018-01-27T12:22:06",
#      "last_account_update": "2018-03-17T22:59:33",
#      "created": "2018-01-23T16:28:18",
#      "mined": false, "owner_challenged": false, "active_challenged": false, "
#      last_owner_proved": "1970-01-01T00:00:00",
#      "last_active_proved": "1970-01-01T00:00:00",
#       "recovery_account": "steem", "last_account_recovery": "1970-01-01T00:00:00",
#        "reset_account": "null", "comment_count": 0, "lifetime_vote_count": 0,
#        "post_count": 114, "can_vote": true, "voting_power": 9001, "last_vote_time":
#         "2018-03-18T09:42:15", "balance": "0.000 STEEM", "savings_balance":
#         "0.000 STEEM", "sbd_balance": "0.205 SBD", "sbd_seconds": "2084413992",
#         "sbd_seconds_last_update": "2018-03-17T21:22:42", "sbd_last_interest_payment":
#          "2018-02-24T13:09:42", "savings_sbd_balance": "0.000 SBD", "savings_sbd_seconds":
#          "0", "savings_sbd_seconds_last_update": "1970-01-01T00:00:00",
#           "savings_sbd_last_interest_payment": "1970-01-01T00:00:00",
#           "savings_withdraw_requests": 0, "reward_sbd_balance": "0.000 SBD",
#           "reward_steem_balance": "0.000 STEEM", "reward_vesting_balance":
#           "2.041180 VESTS", "reward_vesting_steem": "0.001 STEEM",
#           "vesting_shares": "153638.111174 VESTS", "delegated_vesting_shares":
#            "0.000000 VESTS", "received_vesting_shares": "241350.811633 VESTS",
#            "vesting_withdraw_rate": "0.000000 VESTS", "next_vesting_withdrawal":
#            "1969-12-31T23:59:59", "withdrawn": 0, "to_withdraw": 0, "withdraw_routes": 0,
#             "curation_rewards": 478, "posting_rewards": 148303, "proxied_vsf_votes": [0, 0, 0, 0],
#             "witnesses_voted_for": 2, "average_bandwidth": "60365881797", "lifetime_bandwidth":
#             "476411000000", "last_bandwidth_update": "2018-03-18T09:42:15", "average_market_bandwidth": 1170000000,
#             "lifetime_market_bandwidth": "32830000000", "last_market_bandwidth_update": "2018-03-15T16:50:24",
#             "last_post": "2018-03-18T09:25:09", "last_root_post": "2018-03-14T21:51:45", "vesting_balance":
#              "0.000 STEEM", "reputation": "2537718240135", "transfer_history": [], "market_history": [],
#               "post_history": [], "vote_history": [], "other_history": [], "witness_votes": ["emrebeyler",
#               "utopian-io"], "tags_usage": [], "guest_bloggers": []}, "username":
#               "hakancelik", "name":
#               "hakancelik", "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYXBwIiwicHJveHkiOiJjb29nZ2VyLmFwcCIsInVzZXIiOiJoYWthbmNlbGlrIiwic2NvcGUiOltdLCJpYXQiOjE1MjEzNjk3ODksImV4cCI6MTUyMTk3NDU4OX0.RUTwpIhPUydtwnx8eAB_j31t9DqhEqm8sWOLB7i_or4",
#               "token_type": null}
