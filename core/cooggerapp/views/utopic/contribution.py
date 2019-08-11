from ...models import Commit
from .commit import Commits


class Contribution(Commits):
    commits = Commit.objects.get_waiting_commits
