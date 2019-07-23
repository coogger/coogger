#django
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

#django libs
from django_page_views.models import DjangoViews

#python
import json

class DetailPostView(object):
    """
    This class provides detail object and make a reply,
    subclass must write a function named get_object
    """

    model = None
    model_name = None
    from_class = None
    template_name = None
    same_fields = list() #fields that remain the same when commented.
    response_field = list() #json respon fields after commented
    update_field = dict() #dict to update fields

    def save_view(self, request, id):
        get_view, created = DjangoViews.objects.get_or_create(
            content_type=ContentType.objects.get(
                app_label="cooggerapp", 
                model=self.model_name
            ), 
            object_id=id
        )
        try:
            get_view.ips.add(request.ip_model)
        except IntegrityError:
            pass

    def get_context_data(self, **kwargs):
        return dict(
            queryset=self.get_object(**kwargs),
            form=self.form_class,
        )

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        queryset = context.get("queryset")
        self.save_view(request, queryset.id)
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        object = self.get_object(**kwargs)
        form = self.form_class(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.reply = object
            for field in self.same_fields:
                setattr(form, field, getattr(object, field))
            for up_value, up_key in self.update_field.items():
                setattr(form, up_value, up_key)
            form.save()
            def get_context_data():
                context = dict()
                for field in self.response_field:
                    s = field.split(".")
                    if len(s) == 1:
                        context[field] = str(getattr(form, field))
                    else:
                        obj = form
                        for f in s:
                            obj = getattr(obj, f)
                        value = str(obj)
                        context[s[-1]] = value
                return context
            return HttpResponse(json.dumps(get_context_data()))
    
