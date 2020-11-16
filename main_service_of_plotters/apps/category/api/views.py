from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from main_service_of_plotters.apps.category.models import (
    DeviceCategory, ModelsTemplate, Manufacturer)
from .serializers import (
    DeviceCategoryListSerializer, ManufacturerListSerializer,
    ModelsTemplateListSerializer, DeviceCategoryInstSerializer,
    ManufacturerInstSerializer)
from main_service_of_plotters.apps.materials.api.serializers import TemplateListSerializer


@permission_classes([IsAuthenticated, DjangoModelPermissions])
class DeviceCategoryViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = DeviceCategoryListSerializer
    queryset = DeviceCategory.objects.all()

    def get_serializer_class(self):
        serializer_class = super().get_serializer_class()

        if self.action == 'retrieve':
            serializer_class = DeviceCategoryInstSerializer

        return serializer_class

    @action(methods=['get'], detail=True)
    def manufacturers(self, request, pk=None):
        category = self.get_object()
        queryset = category.device.all()
        seria = ManufacturerListSerializer(queryset, many=True, context={'request': request})
        return Response(seria.data)


@permission_classes([IsAuthenticated, DjangoModelPermissions])
class ManufacturerViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = ManufacturerListSerializer
    queryset = Manufacturer.objects.all()

    def get_serializer_class(self):
        serializer_class = super().get_serializer_class()

        if self.action == 'retrieve':
            serializer_class = ManufacturerInstSerializer

        return serializer_class

    @action(methods=['get'], detail=True)
    def models(self, request, pk=None):
        manufacturer = self.get_object()
        queryset = manufacturer.modelstemplate.all()
        seria = ModelsTemplateListSerializer(queryset, many=True, context={'request': request})
        return Response(seria.data)


@permission_classes([IsAuthenticated, DjangoModelPermissions])
class ModelsTemplateViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = ModelsTemplateListSerializer
    queryset = ModelsTemplate.objects.all()

    @action(methods=['get'], detail=True)
    def templates(self, request, pk=None):
        model = self.get_object()
        queryset = model.template_set.all()
        seria = TemplateListSerializer(queryset, many=True, context={'request': request})
        return Response(seria.data)
