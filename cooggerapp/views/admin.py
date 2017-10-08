from django.http import *
from django.shortcuts import render
from django.contrib.auth import *
from cooggerapp.choices import *
from cooggerapp.views.tools import make_choices

def chose_subcategory(request,value): 
    "value ile gelen fields kodunu alıp ilgili bir alt dalı seçip gönderiyorum"
    if not request.is_ajax():
        return None
    values = []
    for i in dir(Subcategory): # burada gelen value bilgisini kontrol ediyoruz ki istenmeyen bir value gelmesin
        if not i.startswith("__"):
            values.append(i)
    value = value.replace("-","_")
    if value not in values:
        return HttpResponse("<option value='' selected='selected'>---------</option>")
    subcategory = make_choices(eval("Subcategory."+value+"()"))
    option = "<option value='' selected='selected'>---------</option>"
    for sub in subcategory:
        option += "<option value='{}'>{}</option>".format(sub[0].lower(),sub[1].lower()) # html format yaptık ve yolladık
    return HttpResponse(option)
        
def chose_category2(request,value):
    if not request.is_ajax():
        return None
    values = []
    for i in dir(Category2): # burada gelen value bilgisini kontrol ediyoruz ki istenmeyen bir value gelmesin
        if not i.startswith("__"):
            values.append(i)
    value = value.replace("-","_")
    if value not in values:
        return HttpResponse("<option value='' selected='selected'>---------</option>")
    category2 = make_choices(eval("Category2."+value+"()"))
    option = "<option value='' selected='selected'>---------</option>"
    for cat in category2:
        option += "<option value='{}'>{}</option>".format(cat[0].lower(),cat[1].lower()) # html format yaptık ve yolladık
    return HttpResponse(option)

def chosenone(request):
    return HttpResponse("<option value='' selected='selected'>---------</option>")