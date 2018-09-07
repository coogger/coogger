def coogger_categories():
    return [
    "science",
    "development",
    "tutorial",
    "idea",
    "project",
    "computer",
    "language",
    "art",
    "technology",
    "biography",
    "books",
    "business",
    "media",
    "travel",
    "health",
    "music",
    "food",
    "history",
    "finance",
    "exchange",
    "design graphic",
    "question answer",
    "translation",
    "discussion",
    ]

def coogger_languages():
    return (
        "english",
        "korean",
        "spanish",
        "turkish",
        "chinese",
        "arabic",
        "french",
        "indonesian",
        "korean",
        "polish",
        "portuguese",
        "german",
        "italian",
        "japanese",
        "romanian",
        "russian",
        "vietnamese ",
        "arabic",
        "azerbaijani",
    )

def follow():
    return (
        "github",
        "linkedin",
        "instagram",
        "facebook",
        "youtube",
        "web site",
    )

def reports():
    return [
    "Fraud or Plagiarism",
    "Hate Speech or Internet Trolling",
    "Intentional miss-categorized content or Spam",
    "This content is not tutorial content",
    "Wrong list name",
    "I think this content should not be at coogger",
    ]

def status_choices():
    return [
    "shared",
    "changed",
    "rejected",
    "approved",
    ]


def make_choices(choice):
    from django.utils.text import slugify
    slugs = []
    for cho in choice:
        cho = str(cho).lower()
        slugs.append((slugify(cho),cho))
    return slugs
