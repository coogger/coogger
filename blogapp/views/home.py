from django.http import *
from django.shortcuts import render
from django.contrib.auth import *
from django.contrib import messages

from django.db.models import F

from blogapp.models import *
from blogapp.forms import *

def home(request):
    queryset = Content.objects.all()
    output = dict(
        queryset = queryset,
    )
    return render(request,"home/home.html",output)
