from ...models import Commit
from .commit import Commits


class Contribution(Commits):
    commits = Commit.objects.waiting_commits.order_by("created")
