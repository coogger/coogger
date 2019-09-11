# Generated by Django 2.0.12 on 2019-09-11 15:46

from django.db import migrations


def create_ghost_user(apps, schema_editor):
    User = apps.get_model("auth", "User")
    UserProfile = apps.get_model("cooggerapp", "UserProfile")
    GithubAuthUser = apps.get_model("github_auth", "GithubAuthUser")
    Follow = apps.get_model("django_follow_system", "Follow")
    ghost_user, _ = User.objects.get_or_create(
        username="ghost", first_name="Deleted", last_name="user"
    )
    UserProfile(
        user=ghost_user,
        email_permission=False,
        bio="Hi, I'm @ghost! I take the place of user accounts that have been deleted. 👻",
    ).save()
    GithubAuthUser(
        user=ghost_user,
        code="",
        access_token="",
        extra_data="""{'login': 'ghost', 'avatar_url': 'https://avatars0.githubusercontent.com/u/10137?s=460&v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/ghost', 'html_url': 'https://github.com/ghost', 'followers_url': 'https://api.github.com/users/ghost/followers', 'following_url': 'https://api.github.com/users/ghost/following{/other_user}', 'gists_url': 'https://api.github.com/users/ghost/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/ghost/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/ghost/subscriptions', 'organizations_url': 'https://api.github.com/users/ghost/orgs', 'repos_url': 'https://api.github.com/users/ghost/repos', 'events_url': 'https://api.github.com/users/ghost/events{/privacy}', 'received_events_url': 'https://api.github.com/users/ghost/received_events', 'type': 'User', 'site_admin': False, 'name': 'Deleted User', 'company': '', 'blog': '', 'location': 'Nothing to see here, move along.', 'email': '', 'hireable': True, 'bio': 'Hi, I"m @ghost! I take the place of user accounts that have been deleted. 👻'}""",
    ).save()
    Follow(user=ghost_user).save()


class Migration(migrations.Migration):

    dependencies = [("cooggerapp", "0006_auto_20190906_1516")]

    operations = [migrations.RunPython(create_ghost_user)]
