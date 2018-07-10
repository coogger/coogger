def steemkitchen_right():
    return [
    "Recipe",
    "Food-Blog",
    "Steemkitchen Contest Entry",
    "Steemit Iron Chef",
    "Cook With Us",
    "Food Photography",
    ]

def coogger_right():
    return [
    "science",
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
    "development",
    "question answer",
    "translation",
    "discussion",
    ]

def coogger_left():
    return (
        "turkish",
        "english",
        "korean",
        "spanish",
        "arabic",
        "french",
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

def steemkitchen_left():
    return coogger_left()

def follow():
    return (
        "facebook",
        "instagram",
        "youtube",
        "github",
        "linkedin",
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

def cantapproved_choices():
    return [
    "It is not information sharing.",
    "It is not tutorial content.",
    "It is not translation"
    "It is tutorial content but not enough, please edit and reshare",
    "It is information sharing but not enough, please edit and reshare",
    "It is translation contribution but not enough, please edit and reshare",
    "Fraud or Plagiarism.",
    "Hate Speech or Internet Trolling.",
    "Intentional miss-categorized content or Spam.",
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
