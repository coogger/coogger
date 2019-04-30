from hashlib import sha256
from uuid import uuid4
from django.utils.text import slugify

__all__ = ["get_new_hash"]


def get_new_hash():
    return sha256(str(uuid4().hex).encode("utf-8")).hexdigest()

def format_tags(tags):
    return " ".join({slugify(tag.lower()) for tag in tags})