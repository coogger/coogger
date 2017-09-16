from django.http import *
from django.shortcuts import render
from django.contrib.auth import *
from blogapp.content_topics import *

def chose_branch(request,value): 
    "value ile gelen fields kodunu alıp ilgili bir alt dalı seçip gönderiyorum"
    if not request.is_ajax():
        return None
    f = Fields.fields
    values = [i[0] for i in f] # burada gelen value bilgisini kontrol ediyoruz ki istenmeyen bir value gelmesin
    if value not in values:
        return None
    brach = eval("Branches."+value) # seçilen field e göre branch ı aldık
    option = ""
    for br in brach:
        option += "<option value='{}'>{}</option>".format(br[0],br[1]) # html format yaptık ve yolladık
    return HttpResponse(option)
        