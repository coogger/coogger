from hashlib import sha256
from uuid import uuid4
from django.utils.text import slugify

def get_new_hash():
    return sha256(str(uuid4().hex).encode("utf-8")).hexdigest()

def format_tags(tags):
    return " ".join({slugify(tag.lower()) for tag in tags})

def second_convert(second):
    second = int(second)
    minutes = int(second / 60)
    second -= minutes * 60
    hours = int(second / (60 * 60))
    second -= hours * (60 * 60)
    days = int(second / (60 * 60 * 24))
    second -= days * (60 * 60 * 24)
    years = int(second / (60 * 60 * 24 * 365.25))
    second -= years * (60 * 60 * 24 * 365.25)
    return dict(years=years, days=days, hours=hours, minutes=minutes, second=int(second))