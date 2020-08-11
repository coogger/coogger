from django.contrib.contenttypes.models import ContentType
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView

from .models import DjangoViews


class GetView(APIView):
    class DjangoViewsSerializer(ModelSerializer):
        class Meta:
            model = DjangoViews
            fields = ("views_count",)

    model = DjangoViews
    serializer_class = DjangoViewsSerializer
    permission_classes = []

    def get(self, request, app_label, model, id):
        queryset = self.model.objects.filter(
            content_type=ContentType.objects.get(
                app_label=app_label, model=model
            ),
            object_id=id,
        )
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
