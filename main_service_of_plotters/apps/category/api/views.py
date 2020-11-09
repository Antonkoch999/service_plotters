from main_service_of_plotters.apps.category.models import (
    DeviceCategory, ModelsTemplate, Manufacturer)
from .serializers import (
    DeviceCategoryListSerializer, ManufacturerListSerializer,
    ModelsTemplateListSerializer, DeviceCategoryInstSerializer,
    ManufacturerInstSerializer)
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework import viewsets


@permission_classes([IsAuthenticated, DjangoModelPermissions])
class DeviceCategoryViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = DeviceCategoryListSerializer
    queryset = DeviceCategory.objects.all()

    def get_serializer_class(self):
        serializer_class = super().get_serializer_class()

        if self.action == 'retrieve':
            serializer_class = DeviceCategoryInstSerializer

        return serializer_class


@permission_classes([IsAuthenticated, DjangoModelPermissions])
class ManufacturerViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = ManufacturerListSerializer
    queryset = Manufacturer.objects.all()

    def get_serializer_class(self):
        serializer_class = super().get_serializer_class()

        if self.action == 'retrieve':
            serializer_class = ManufacturerInstSerializer

        return serializer_class


@permission_classes([IsAuthenticated, DjangoModelPermissions])
class ModelsTemplateViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = ModelsTemplateListSerializer
    queryset = ModelsTemplate.objects.all()
