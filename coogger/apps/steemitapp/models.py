from django.db import models
from django.db.models import F

class SearchedWords(models.Model):
    word = models.CharField(unique=True,max_length=310)
    hmany = models.IntegerField(default = 1)

    def save(self, *args, **kwargs):
        data_search = SearchedWords.objects.filter(word = self.word)
        if data_search.exists():
            data_search = data_search[0]
            data_search.hmany = F("hmany") + 1
            data_search.save()
        else:
            super(SearchedWords, self).save(*args, **kwargs)
