from django.conf import settings


def search_info(request):
    return {"MINIMUM_SEARCH_LENGTH": settings.MINIMUM_SEARCH_LENGTH}
