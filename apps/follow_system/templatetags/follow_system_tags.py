from django import template

register = template.Library()


@register.filter(name="following_count")
def following_count(user):
    if user.is_anonymous:
        return 0
    return user.follow.following.count()


@register.filter(name="followers_count")
def follower_count(user):
    if user.is_anonymous:
        return 0
    return user.follow.follower.count()


@register.filter(name="is_follow")
def is_follow(user, other_user):
    return user.follow.is_follow(other_user)
