from main_service_of_plotters.apps.materials.models import Template, Label
from rest_framework.viewsets import ModelViewSet
from .serializers import (TemplateListSerializer, LabelListSerializer)
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password


class TemplateViewSet(ModelViewSet):
    serializer_class = TemplateListSerializer
    queryset = Template.objects.all()


class LabelViewSet(ModelViewSet):
    serializer_class = LabelListSerializer
    queryset = Label.objects.all()
