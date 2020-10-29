from main_service_of_plotters.apps.category.models import (
    DeviceCategory, ModelsTemplate, Manufacturer)
from rest_framework.viewsets import ModelViewSet
from .serializers import (
    DeviceCategoryListSerializer, ManufacturerListSerializer,
    ModelsTemplateListSerializer)
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password


class DeviceCategoryViewSet(ModelViewSet):
    serializer_class = DeviceCategoryListSerializer
    queryset = DeviceCategory.objects.all()


class ManufacturerViewSet(ModelViewSet):
    serializer_class = ManufacturerListSerializer
    queryset = Manufacturer.objects.all()


class ModelsTemplateViewSet(ModelViewSet):
    serializer_class = ModelsTemplateListSerializer
    queryset = ModelsTemplate.objects.all()
