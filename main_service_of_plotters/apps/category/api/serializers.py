"""This module serializer data of the category model."""

from rest_framework import serializers, fields
from rest_framework.reverse import reverse
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes

from main_service_of_plotters.apps.category.models import (
    DeviceCategory, Manufacturer, ModelsTemplate)


class DeviceCategoryListSerializer(serializers.HyperlinkedModelSerializer):
    """This class serializes of device category model."""

    manufacturers = fields.SerializerMethodField()

    class Meta:
        """Metadata of device category."""

        model = DeviceCategory
        fields = ['id', 'name', 'photo', 'url', 'manufacturers']
        extra_kwargs = {
            'url': {'view_name': 'api:devicecategory-detail'},
        }

    @extend_schema_field(OpenApiTypes.URI)
    def get_manufacturers(self, obj) -> str:
        """Create link for device category with a list manufacturers.

        :param obj: instance device category
        :return: string format: /api/devicecategory/{id}/manufacturers/
        """
        return reverse('api:devicecategory-manufacturers', [obj.pk],
                       request=self.context['request'])


class DeviceCategoryInstSerializer(serializers.HyperlinkedModelSerializer):
    """This class serializes of one device category model."""

    manufacturers = fields.SerializerMethodField()

    class Meta:
        """Metadata of device category."""

        model = DeviceCategory
        fields = ['id', 'name', 'photo', 'url', 'device', 'manufacturers']
        extra_kwargs = {
            'url': {'view_name': 'api:devicecategory-detail'},
            'device': {'view_name': 'api:manufacturer-detail'},
        }

    @extend_schema_field(OpenApiTypes.URI)
    def get_manufacturers(self, obj) -> str:
        """Create link for device category with a list manufacturers.

        :param obj: instance device category
        :return: string format: /api/devicecategory/{id}/manufacturers/
        """
        return reverse('api:devicecategory-manufacturers', [obj.pk],
                       request=self.context['request'])

class ManufacturerListSerializer(serializers.HyperlinkedModelSerializer):
    """This class serializes of manufacturers model."""

    models = fields.SerializerMethodField()

    class Meta:
        """Metadata of manufacturer."""

        model = Manufacturer
        fields = ['id', 'device_category', 'name', 'photo', 'url', 'models']
        extra_kwargs = {
            'url': {'view_name': 'api:manufacturer-detail'},
            'device_category': {'view_name': 'api:devicecategory-detail'},
        }

    @extend_schema_field(OpenApiTypes.URI)
    def get_models(self, obj) -> str:
        """Create link for manufacturer with a list models template.

        :param obj: instance manufacturer
        :return: string format: /api/manufacturer/{id}/model/
        """
        return reverse('api:manufacturer-models', [obj.pk],
                       request=self.context['request'])


class ManufacturerInstSerializer(serializers.HyperlinkedModelSerializer):
    """This class serializes of one manufacturers model."""

    models = fields.SerializerMethodField()

    class Meta:
        """Metadata of manufacturer."""

        model = Manufacturer
        fields = ['id', 'device_category', 'name', 'photo', 'url',
                  'modelstemplate', 'models']
        extra_kwargs = {
            'url': {'view_name': 'api:manufacturer-detail'},
            'device_category': {'view_name': 'api:devicecategory-detail'},
            'modelstemplate': {'view_name': 'api:modelstemplate-detail'},
        }

    @extend_schema_field(OpenApiTypes.URI)
    def get_models(self, obj):
        """Create link for manufacturer with a list models template.

        :param obj: instance manufacturer
        :return: string format: /api/manufacturer/{id}/model/
        """
        return reverse('api:manufacturer-models', [obj.pk],
                       request=self.context['request'])


class ModelsTemplateListSerializer(serializers.HyperlinkedModelSerializer):
    """This class serializes of models template model."""

    templates = fields.SerializerMethodField()

    class Meta:
        """Metadata of models template."""

        model = ModelsTemplate
        fields = ['id', 'manufacturer', 'name', 'url', 'template_set',
                  'templates']
        extra_kwargs = {
            'url': {'view_name': 'api:modelstemplate-detail'},
            'manufacturer': {'view_name': 'api:manufacturer-detail'},
            'template_set': {'view_name': 'api:template-detail'}
        }

    @extend_schema_field(OpenApiTypes.URI)
    def get_templates(self, obj):
        """Create link for models template with a list template.

        :param obj: instance models template
        :return: string format: /api/modelstemplate/{id}/templates/
        """
        return reverse('api:modelstemplate-templates', [obj.pk],
                       request=self.context['request'])
