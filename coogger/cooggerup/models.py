# from django.db import models
# from django.db.models import F
#
# class SearchedWords(models.Model):
#     word = models.CharField(unique=True,max_length=310)
#     hmany = models.IntegerField(default = 1)
#
#     def save(self, *args, **kwargs):
#         try:
#             super(SearchedWords, self).save(*args, **kwargs)
#         except:
#             SearchedWords.objects.filter(word = self.word).update(hmany = F("hmany") + 1)
