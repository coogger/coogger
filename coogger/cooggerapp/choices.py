steemkitchen_categories = [
    "Recipe",
    "Food Blog",
    "Contest Entry",
    "Steemit Iron Chef",
    "Cook With Us",
    "Food Photography",
    ]

coogger_categories = [
    "development",
    "tutorial",
    "project",
    "graphics",
    "documentation",
    "science",
    "idea",
    "travel",
    "music",
    "analysis",
    "blog",
    "bug-hunting",
    "computer",
    "language",
    "art",
    "technology",
    "biography",
    "books",
    "food",
    "history",
    "finance",
    "exchange",
    "translation",
    ]

letsteem_categories = [
    "car",
    "estate",
    "free",
    "technology",
    "vehicle",
    "sports",
    "home",
    "fun",
    "fashion",
    "kid",
    "service",
    "other",
    ]

all_categories = coogger_categories + steemkitchen_categories + letsteem_categories

languages = [
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
    ]

follow = [
        "github",
        "linkedin",
        "instagram",
        "facebook",
        "youtube",
        "web site",
    ]

reports = [
    "Fraud or Plagiarism",
    "Hate Speech or Internet Trolling",
    "Intentional miss-categorized content or Spam",
    "This content is not tutorial content",
    "Wrong list name",
    "I think this content should not be at coogger",
    ]

status_choices = [
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
