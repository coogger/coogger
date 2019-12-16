from django.contrib.contenttypes.models import ContentType


def get_content_type(app_label, model):
    return ContentType.objects.get(app_label=app_label, model=model)


def get_content_type_with_model(model):
    content_type_obj = ContentType.objects.get_for_model(model)
    return get_content_type(content_type_obj.app_label, content_type_obj.model)


def get_model(app_label, model, id):
    model = get_content_type(app_label, model).model_class()
    return model.objects.get(id=id)
