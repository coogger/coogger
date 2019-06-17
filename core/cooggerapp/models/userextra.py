# django 
from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import m2m_changed, post_save
from django.db.utils import IntegrityError


# models
from .topic import UTopic

# 3.part 
from django_md_editor.models import EditorMdField
from django_follow_system.models import Follow
from github_auth.models import GithubAuthUser

# choices
from core.cooggerapp.choices import FOLLOW, make_choices

# python
import requests

# utils
from .utils import send_mail, get_client_url

class OtherAddressesOfUsers(models.Model):
    "maybe ManyToManyField in UserProfile"
    choices = models.CharField(
        blank=True,
        null=True,
        max_length=15,
        choices=make_choices(FOLLOW),
        verbose_name="website",
    )
    address = models.CharField(
        blank=True, null=True, max_length=50, verbose_name="write address / username"
    )

    def __str__(self):
        return f"{self.choices} - {self.address}"

    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = EditorMdField(blank=True, null=True)
    address = models.ManyToManyField(
        OtherAddressesOfUsers,
        blank=True,
    )
    email_permission = models.BooleanField(default=True)


def save_github_follow(user):
    url = user.githubauthuser.get_extra_data_as_dict.get("url")
    following = [following_user.get("login").lower() \
        for following_user in requests.get(url + "/following" + get_client_url()).json()]
    for following_username in following:
        following_user = User.objects.filter(username=following_username)
        if following_user.exists():
            try:
                user.follow.following.add(following_user[0])
            except IntegrityError:
                pass
    followers = [follower_user.get("login").lower() \
        for follower_user in requests.get(url + "/followers" + get_client_url()).json()]
    for follower_username in followers:
        follow_user = User.objects.filter(username=follower_username)
        if follow_user.exists():
            try:
                follow_user[0].follow.following.add(user)
            except IntegrityError:
                pass

def save_github_repos(user, github_repos_url):
    for repo in requests.get(github_repos_url + get_client_url()).json():
        if repo.get("fork") == False:
            try:
                UTopic(
                    user=user, 
                    name=repo.get("name"), 
                    definition=repo.get("description"), 
                    address=repo.get("html_url"), 
                ).save()
            except IntegrityError:
                pass

def save_github_org(user):
    organizations_url = user.githubauthuser.get_extra_data_as_dict.get("organizations_url")
    for org in requests.get(organizations_url + get_client_url()).json():
        save_github_repos(user, org.get("repos_url"))

@receiver(post_save, sender=GithubAuthUser)
def follow_and_repos_update(sender, instance, created, **kwargs):
    user = User.objects.get(username=instance.user.username)
    save_github_follow(user)
    github_repos_url = user.githubauthuser.get_extra_data_as_dict.get("repos_url")
    save_github_repos(user, github_repos_url)
    save_github_org(user)
    if created:
        send_mail(
            subject=f"{user} has entered the coogger | coogger".title(), 
            template_name="email/first_login.html", 
            context=dict(
                user=user
            )
            to=[user.email], 
        )   

@receiver(post_save, sender=User)
def create_userprofile(sender, instance, created, **kwargs):
    if created:
        UserProfile(user=instance).save()
        
@receiver(m2m_changed, sender=Follow.following.through)
def send_mail_to_follow(sender, **kwargs):
    action = kwargs.get("action", None)
    if action == "pre_add":
        instance = kwargs.get("instance", None)
        for follow_id in kwargs.get("pk_set", None):
            to = list()
            for u in Follow.objects.get(id=follow_id).user.follow.follower:
                email = u.user.email
                if email:
                    to.append(email)
            send_mail(
                subject=f"{instance.user} started to follow you | coogger".title(), 
                template_name="email/follow.html", 
                context=dict(
                    user=instance.user
                ),
                to=to
            )