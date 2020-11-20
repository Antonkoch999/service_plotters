"""This module contents view methods for category."""

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from main_service_of_plotters.apps.category.models import (
    DeviceCategory, ModelsTemplate, Manufacturer)
from main_service_of_plotters.apps.materials.api.serializers import TemplateListSerializer
from .serializers import (
    DeviceCategoryListSerializer, ManufacturerListSerializer,
    ModelsTemplateListSerializer, DeviceCategoryInstSerializer,
    ManufacturerInstSerializer)


@permission_classes([IsAuthenticated, DjangoModelPermissions])
class DeviceCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """This class is read only device category."""

    serializer_class = DeviceCategoryListSerializer
    queryset = DeviceCategory.objects.all()

    def get_serializer_class(self) -> classmethod:
        """Return the class to use for the serializer.

        :return: serializer_class depending on action
        """
        serializer_class = super().get_serializer_class()

        if self.action == 'retrieve':
            serializer_class = DeviceCategoryInstSerializer

        return serializer_class

    @action(methods=['get'], detail=True)
    def manufacturers(self, request, pk=None) -> Response:
        """Return full list manufacturers related with device category.

        :param request: instance model device category
        :param pk: We don't know, it is django documentations
        :return: full list manufacturers
        """
        category = self.get_object()
        queryset = category.device.all()
        seria = ManufacturerListSerializer(queryset, many=True,
                                           context={'request': request})
        return Response(seria.data)


@permission_classes([IsAuthenticated, DjangoModelPermissions])
class ManufacturerViewSet(viewsets.ReadOnlyModelViewSet):
    """This class is read only model manufacturer."""

    serializer_class = ManufacturerListSerializer
    queryset = Manufacturer.objects.all()

    def get_serializer_class(self) -> classmethod:
        """Return the class to use for the serializer.

        :return: serializer_class depending on action
        """
        serializer_class = super().get_serializer_class()

        if self.action == 'retrieve':
            serializer_class = ManufacturerInstSerializer

        return serializer_class

    @action(methods=['get'], detail=True)
    def models(self, request, pk=None) -> Response:
        """Return full list models template related with manufacturer.

        :param request: instance model manufacturer
        :param pk: We don't know, it is django documentations
        :return: full list models template
        """
        manufacturer = self.get_object()
        queryset = manufacturer.modelstemplate.all()
        seria = ModelsTemplateListSerializer(queryset, many=True,
                                             context={'request': request})
        return Response(seria.data)


@permission_classes([IsAuthenticated, DjangoModelPermissions])
class ModelsTemplateViewSet(viewsets.ReadOnlyModelViewSet):
    """This class is read only model models template."""

    serializer_class = ModelsTemplateListSerializer
    queryset = ModelsTemplate.objects.all()

    @action(methods=['get'], detail=True)
    def templates(self, request, pk=None) -> Response:
        """Return full list template related with models template.

        :param request: instance model models template
        :param pk: We don't know, it is django documentations
        :return: full list template
        """
        model = self.get_object()
        queryset = model.template_set.all()
        seria = TemplateListSerializer(queryset, many=True,
                                       context={'request': request})
        return Response(seria.data)
