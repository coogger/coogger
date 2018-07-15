from django.db import models
from django.contrib.auth.models import User

class SteemConnectUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    refresh_token = models.CharField(max_length = 500,help_text = "steemconnect user code / to get get_refresh_token")
    code = models.CharField(max_length = 500,help_text = "steemconnect user code / to get get_refresh_token")
    access_token = models.CharField(max_length = 500,help_text = "steemconnect user access_token to any operations")
    community_name = models.CharField(max_length = 100,help_text = "community name")

    @property
    def username(self):
        return self.user.username
