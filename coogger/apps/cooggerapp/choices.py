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

def approved_choices():
    return [
    "information sharing",
    "tutorial content",
    "translation", # çok lu dil özelliği gelince olacak.
    ]

def make_choices(choice):
    from django.utils.text import slugify
    slugs = []
    for cho in choice:
        cho = str(cho).lower()
        slugs.append((slugify(cho),cho))
    return slugs
