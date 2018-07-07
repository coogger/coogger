#django
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render
from django.db.models import F
from django.contrib import messages as ms

# class
#from django.views.generic import ListView
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

#models
from cooggerapp.models import Content

#form
from cooggerapp.forms import ContentForm

# view
from cooggerapp.views.tools import get_community_model

#steem
from steem.post import Post


class Create(View):
    template_name = "controls/create.html"

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        community_model = get_community_model(request)
        return render(request, self.template_name, {"form":ContentForm(),"community":community_model})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = ContentForm(request.POST)
        if form.is_valid():
            form = form.save(commit = False)
            form.user = request.user
            save = form.content_save(request) # save with sc2py and get ms
            if save.status_code != 200: # if any error show the error
                ms.error(request,save.text)
                return self.create_error(request)
            return HttpResponseRedirect("/"+form.get_absolute_url())
        else:
            return self.create_error(request)

    def create_error(self,request):
        ms.error(request, "unexpected error, check your content please or contact us on discord; <a gnrl='c-primary' href='https://discord.gg/q2rRY8Q'>https://discord.gg/q2rRY8Q</a>")
        return render(request, self.template_name, {"form":ContentForm(request.POST)})


class Change(View):
    template_name = "controls/change.html"

    @method_decorator(login_required)
    def get(self, request, content_id, *args, **kwargs):
        self.content_update(request,content_id)
        community_model = get_community_model(request)
        queryset = Content.objects.filter(community = community_model,user = request.user,id = content_id)[0]
        content_form = ContentForm(instance=queryset)
        context = dict(
            community = community_model,
            content_id = content_id,
            form = content_form,
        )
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, content_id, *args, **kwargs):
        form = ContentForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            queryset = Content.objects.filter(user = request.user,id = content_id)
            save = form.content_update(request,queryset,form) # save with sc2py and get ms
            if save.status_code != 200:
                ms.error(request,save.text)
                return self.create_error(request)
            return HttpResponseRedirect("/"+queryset[0].get_absolute_url())

    @staticmethod
    def content_update(request,content_id):
        ct = Content.objects.filter(user = request.user,id = content_id)
        steem = Post(post = ct[0].get_absolute_url())
        ct.update(content = steem.body,title = steem.title)

    def create_error(self,request):
        ms.error(request, "unexpected error, check your content please or contact us on discord; <a gnrl='c-primary' href='https://discord.gg/q2rRY8Q'>https://discord.gg/q2rRY8Q</a>")
        return render(request, self.template_name, {"form":ContentForm(request.POST)})
