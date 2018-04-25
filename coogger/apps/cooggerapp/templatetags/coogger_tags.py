from django import template

register = template.Library()

@register.filter(name="upvote")
def upvote(value, arg):
    return value.upvote(arg)
