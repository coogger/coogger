from django.shortcuts import render
from django.urls import resolve


def just_redirect_by_name(request):
    url_name = resolve(request.path_info).url_name
    return render(request, f"{url_name}.html", {})
