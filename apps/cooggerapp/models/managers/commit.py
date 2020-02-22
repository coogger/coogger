from django.db import models


class StatusQuerySet(models.QuerySet):
    def approved(self):
        return self.filter(status="approved")

    def waiting(self):
        return self.filter(status="waiting")

    def rejected(self):
        return self.filter(status="rejected")


class CommitManager(models.Manager):
    def get_queryset(self):
        return StatusQuerySet(self.model, using=self._db)

    @property
    def approved_commits(self):
        return self.get_queryset().approved()

    @property
    def waiting_commits(self):
        return self.get_queryset().waiting()

    @property
    def rejected_commits(self):
        return self.get_queryset().rejected()
