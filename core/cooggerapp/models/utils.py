# django
from hashlib import sha256
from uuid import uuid4
from django.utils.text import slugify
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# python
from bs4 import BeautifulSoup
from mistune import Markdown, Renderer

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
    return dict(y=years, d=days, h=hours, m=minutes, s=int(second))

def marktohtml(marktext):
    renderer = Renderer(escape=False, parse_block_html=True)
    markdown = Markdown(renderer=renderer)
    return BeautifulSoup(markdown(marktext), "html.parser")

def get_first_image(soup):
    img = soup.find("img")
    context = dict(src="", alt="")
    if img is not None:
        context.update(src=img.get("src", ""))
        context.update(alt=img.get("alt", ""))
    return context

def content_definition(body):
    soup = marktohtml(body)
    first_image = get_first_image(soup)
    src, alt = first_image.get("src"), first_image.get("alt")
    if src:
        return f"<img class='definition-img' src='{src}' alt='{alt}'></img><p>{soup.text[:200]}...</p>"
    return f"<p>{soup.text[0:200]}...</p>"

def dor(body):
    "duration of read -> second"
    return body.__len__() / 28

class NextOrPrevious:

    def __init__(self, model, filter_field, id):
        self.model = model
        self.filter_field = filter_field
        self.id = id

    def next_or_previous(self, next=True):
        queryset = self.model.objects.filter(**self.filter_field)
        try:
            index = list(queryset).index(queryset.filter(id=self.id)[0])
        except IndexError:
            return False
        else:
            if next:
                index = index - 1
            else:
                index = index + 1
        try:
            return queryset[index]
        except (IndexError, AssertionError):
            return False

    @property
    def next_query(self):
        return self.next_or_previous()

    @property
    def previous_query(self):
        return self.next_or_previous(False)

def send_mail(subject, template_name, context, to):
    html_content = render_to_string(template_name, context)
    text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def get_client_url():
    return f"?client_id={settings.GITHUB_AUTH.get('client_id')}&client_secret={settings.GITHUB_AUTH.get('client_secret')}"

def ready_tags(tags, limit=5):
    return format_tags(tags.split(" ")[:limit])