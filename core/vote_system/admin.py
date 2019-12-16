from django.contrib.admin import site

from .models import Vote, VoteCount

site.register(Vote)
site.register(VoteCount)
