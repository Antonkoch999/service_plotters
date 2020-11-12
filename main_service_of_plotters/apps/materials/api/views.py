from rest_framework.viewsets import ModelViewSet

from main_service_of_plotters.apps.materials.models import Template, Label
from .serializers import (TemplateListSerializer, LabelListSerializer)


class TemplateViewSet(ModelViewSet):
    serializer_class = TemplateListSerializer
    queryset = Template.objects.all()


class LabelViewSet(ModelViewSet):
    serializer_class = LabelListSerializer
    queryset = Label.objects.all()
