from django.http import *
from django.shortcuts import render
from django.contrib import messages
from cooggerapp.models import *
from django.db.models import Q


def topic(request,topic):
    model = Blog 
    querset = model.objects.filter(category = topic)