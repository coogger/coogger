import requests
from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed, post_save
from django.db.utils import IntegrityError
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from github_auth.models import GithubAuthUser

from core.follow_system.models import Follow

from ..models import UserProfile, UTopic, get_client_url, send_mail


def save_github_follow(user):
    url = user.githubauthuser.get_extra_data_as_dict.get("url")
    following = [
        following_user.get("login").lower()
        for following_user in requests.get(url + "/following" + get_client_url()).json()
    ]
    for following_username in following:
        following_user = User.objects.filter(
            is_active=True, username=following_username
        )
        if following_user.exists():
            try:
                user.follow.following.add(following_user[0])
            except IntegrityError:
                pass
    followers = [
        follower_user.get("login").lower()
        for follower_user in requests.get(url + "/followers" + get_client_url()).json()
    ]
    for follower_username in followers:
        follow_user = User.objects.filter(is_active=True, username=follower_username)
        if follow_user.exists():
            try:
                follow_user[0].follow.following.add(user)
            except IntegrityError:
                pass


def save_github_repos(user, github_repos_url):
    for repo in requests.get(github_repos_url + get_client_url()).json():
        if not repo.get("fork"):
            UTopic.objects.get_or_create(
                user=user,
                permlink=slugify(repo.get("name")),
                defaults={
                    "name": repo.get("name"),
                    "description": repo.get("description"),
                    "address": repo.get("html_url"),
                },
            )


@receiver(post_save, sender=GithubAuthUser)
def follow_and_repos_update(sender, instance, created, **kwargs):
    "Works when users every login"
    if instance.user.username == "ghost":
        return
    user = get_object_or_404(User, username=instance.user.username)
    user_extra_data = user.githubauthuser.get_extra_data_as_dict
    save_github_follow(user)
    save_github_repos(user, user_extra_data.get("repos_url"))
    # userprofile.company = user_extra_data.get("company") TODO
    if created:
        userprofile = UserProfile.objects.get(user=instance.user)
        userprofile.bio = user_extra_data.get("bio")
        send_mail(
            subject=f"{user} has entered the coogger | coogger".title(),
            template_name="email/first_login.html",
            context=dict(user=user),
            to=[user],
        )
        userprofile.save()


@receiver(post_save, sender=User)
def create_userprofile(sender, instance, created, **kwargs):
    if created:
        UserProfile(user=instance).save()


@receiver(m2m_changed, sender=Follow.following.through)
def send_mail_to_follow(sender, **kwargs):
    action = kwargs.get("action", None)
    model = kwargs.get("model", None)
    instance = kwargs.get("instance", None)
    pk_set = kwargs.get("pk_set", None)
    if action == "pre_add" and model == User:
        to = list()
        for user_pk in pk_set:
            user = model.objects.get(pk=user_pk)
            if user.email:
                to.append(user)
        send_mail(
            subject=f"{instance.user} started to follow you | coogger".title(),
            template_name="email/follow.html",
            context=dict(user=instance.user),
            to=to,
        )
