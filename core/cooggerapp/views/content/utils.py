from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse


def redirect_utopic(request, utopic_permlink):
    messages.warning(request, f"you need to create the {utopic_permlink} topic first.")
    return redirect(reverse("create-utopic") + f"?name={utopic_permlink}")
