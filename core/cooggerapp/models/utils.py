from hashlib import sha256
from uuid import uuid4

__all__ = ["get_new_hash"]


def get_new_hash():
    return sha256(str(uuid4().hex).encode("utf-8")).hexdigest()
