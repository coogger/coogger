# TODO:  burayı bir güzelliştir

# django
from django.http import *
from django.shortcuts import render
from django.contrib.auth import *
from django.contrib import messages as ms
from django.contrib.auth.models import User
from django.core.exceptions import FieldDoesNotExist

# django class based
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic.base import TemplateView

# models
from cooggerapp.models import Content, Topic
from steemconnect_auth.models import Dapp

# views
from cooggerapp.views.tools import paginator

# form
from cooggerapp.forms import TopicForm

class TopicView(View):
    template_name = "topic/index.html"

    def get(self, request, topic, *args, **kwargs):
        if topic:
            if self.request.dapp_model.name == "coogger":
                queryset = Content.objects.filter(topic=topic, status="approved")
            else:
                queryset = Content.objects.filter(dapp=self.request.dapp_model, topic=topic, status="approved")
            info_of_cards = paginator(self.request, queryset)
            topic_query = Topic.objects.filter(name=topic)[0]
            if topic_query.edit == "false":
                context = dict(
                    content=info_of_cards,
                    topic=topic_query,
                )
                return render(request, self.template_name, context)
            else:
                return render(
                    request, self.template_name, {
                        "content":info_of_cards,
                        "topic_name":topic,
                        "topic_form": TopicForm(
                            initial={
                                "image_address": topic_query.image_address,
                                "definition":topic_query.definition
                                }
                            )
                        }
                    )
        return HttpResponseRedirect("/")

    def post(self, request, topic, *args, **kwargs):
        topic_form = TopicForm(request.POST)
        if topic_form.is_valid():
            topic_form = topic_form.save(commit=False)
            topic_form.name = topic
            topic_query = Topic.objects.filter(name=topic)
            if topic_query.exists():
                items = self.request.POST.items()
                for attr, value in items:
                    try:
                        topic_query.update(**{attr: value})
                    except FieldDoesNotExist:
                        pass
            else: # is that a possible
                topic_form.save()
            return HttpResponseRedirect(f"/topic/{topic}")
        else:
            ms.error(request, topic_form)
            return HttpResponseRedirect(f"/topic/{topic}")


class Hashtag(TemplateView):
    template_name = "card/blogs.html"

    def get_context_data(self, hashtag, **kwargs):
        if hashtag:
            if self.request.dapp_model.name == "coogger":
                queryset = Content.objects.filter(tag__contains=hashtag, status="approved")
            else:
                queryset = Content.objects.filter(dapp=self.request.dapp_model, tag__contains=hashtag, status="approved")
            info_of_cards = paginator(self.request, queryset)
            context = super(Hashtag, self).get_context_data(**kwargs)
            context["content"] = info_of_cards
            context["nameofhashtag"] = hashtag
            return context
        return HttpResponseRedirect("/")


class Languages(TemplateView):
    # TODO:  do language check,  is it necessary ?
    template_name = "card/blogs.html"

    def get_context_data(self, lang_name, **kwargs):
        if lang_name:
            if self.request.dapp_model.name == "coogger":
                queryset = Content.objects.filter(language=lang_name, status="approved")
            else:
                queryset = Content.objects.filter(dapp=self.request.dapp_model, language=lang_name, status="approved")
            info_of_cards = paginator(self.request, queryset)
            context = super(Languages, self).get_context_data(**kwargs)
            context["content"] = info_of_cards
            context["language"] = lang_name
            return context
        return HttpResponseRedirect("/")


class Categories(TemplateView):
    template_name = "card/blogs.html"
    ctof = Content.objects.filter

    def get_context_data(self, cat_name, **kwargs):
        if cat_name:
            if self.request.dapp_model.name == "coogger":
                queryset = self.ctof(category=cat_name, status="approved")
            else:
                queryset = self.ctof(dapp=self.request.dapp_model, category=cat_name, status="approved")
            info_of_cards = paginator(self.request, queryset)
            context = super(Categories, self).get_context_data(**kwargs)
            context["content"] = info_of_cards
            context["category"] = cat_name
            return context
        return HttpResponseRedirect("/")


class Filter(TemplateView):
    template_name = "card/blogs.html"
    queryset = Content.objects.filter(status="approved")

    def get_context_data(self, **kwargs):
        filter = ""
        for attr, value in self.request.GET.items():
            if attr and value:
                filter += f"&{attr}={value}"
                if attr == "username":
                    value = User.objects.filter(username=value)[0]
                    attr = "user"
                elif attr == "dapp":
                    value = Dapp.objects.filter(name=value)[0]
                try:
                    self.queryset = self.queryset.filter(**{attr: value})
                except FieldError:
                    pass
        context = super(Filter, self).get_context_data(**kwargs)
        context["content"] = paginator(self.request, self.queryset)
        context["filter"] = filter
        return context
