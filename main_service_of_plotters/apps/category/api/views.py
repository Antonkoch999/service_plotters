from main_service_of_plotters.apps.category.models import (
    DeviceCategory, ModelsTemplate, Manufacturer)
from .serializers import (
    DeviceCategoryListSerializer, ManufacturerListSerializer,
    ModelsTemplateListSerializer)
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .permissions import AdministratorPermission


@permission_classes([IsAuthenticated, AdministratorPermission])
class DeviceCategoryViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = DeviceCategoryListSerializer
    queryset = DeviceCategory.objects.all()


@permission_classes([IsAuthenticated, AdministratorPermission])
class ManufacturerViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = ManufacturerListSerializer
    queryset = Manufacturer.objects.all()


@permission_classes([IsAuthenticated, AdministratorPermission])
class ModelsTemplateViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = ModelsTemplateListSerializer
    queryset = ModelsTemplate.objects.all()
