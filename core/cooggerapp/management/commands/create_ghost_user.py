from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from github_auth.models import GithubAuthUser


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        ghost_user, get_create = User.objects.get_or_create(
            username="ghost", first_name="Deleted", last_name="user"
        )
        if get_create:
            print("User already saved")
        else:
            print("User saved")
        userprofile = ghost_user.userprofile
        userprofile.email_permission = False
        userprofile.bio = "Hi, I'm @ghost! I take the place of user accounts that have been deleted. 👻"
        userprofile.save()
        print("User Profile updated")
        try:
            GithubAuthUser(
                user=ghost_user,
                code="",
                access_token="",
                extra_data="""{'login': 'ghost', 'avatar_url': 'https://avatars0.githubusercontent.com/u/10137?s=460&v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/ghost', 'html_url': 'https://github.com/ghost', 'followers_url': 'https://api.github.com/users/ghost/followers', 'following_url': 'https://api.github.com/users/ghost/following{/other_user}', 'gists_url': 'https://api.github.com/users/ghost/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/ghost/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/ghost/subscriptions', 'organizations_url': 'https://api.github.com/users/ghost/orgs', 'repos_url': 'https://api.github.com/users/ghost/repos', 'events_url': 'https://api.github.com/users/ghost/events{/privacy}', 'received_events_url': 'https://api.github.com/users/ghost/received_events', 'type': 'User', 'site_admin': False, 'name': 'Deleted User', 'company': '', 'blog': '', 'location': 'Nothing to see here, move along.', 'email': '', 'hireable': True, 'bio': 'Hi, I"m @ghost! I take the place of user accounts that have been deleted. 👻'}""",
            ).save()
        except IntegrityError:
            print("GithubAuthUser already saved")
        else:
            print("GithubAuthUser saved")
