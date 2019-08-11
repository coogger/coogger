from django.utils.text import slugify

LANGUAGES = [
    "arabic",
    "azerbaijani",
    "chinese",
    "english",
    "french",
    "german",
    "indonesian",
    "italian",
    "japanese",
    "korean",
    "polish",
    "portuguese",
    "romanian",
    "russian",
    "spanish",
    "turkish",
    "vietnamese",
]
FOLLOW = [
    "facebook",
    "github",
    "instagram",
    "linkedin",
    "twitter",
    "web site",
    "youtube",
]
REPORTS = [
    "Fraud or Plagiarism",
    "Hate Speech or Internet Trolling",
    "Intentional miss-categorized content or Spam",
    "I think this content should not be at coogger",
    "This content is not tutorial content",
    "Wrong list name",
]
STATUS_CHOICES = ["ready", "not ready"]
COMMIT_STATUS_CHOICES = ["approved", "rejected", "waiting"]
ISSUE_CHOICES = ["open", "closed"]


def make_choices(choice):
    slugs = []
    for cho in choice:
        cho = str(cho).lower()
        slugs.append((slugify(cho), cho))
    return slugs
