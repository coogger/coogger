# django
from django.db import models


class SearchedWords(models.Model):
    word = models.CharField(unique=True, max_length=100)
    hmany = models.IntegerField(default=1)

    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
        except:
            self.__class__.objects.filter(word=self.word).update(
                hmany=models.F("hmany") + 1
            )
