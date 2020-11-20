from rest_framework import serializers, fields
from rest_framework.reverse import reverse
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes

from main_service_of_plotters.apps.category.models import (
    DeviceCategory, Manufacturer, ModelsTemplate)


class DeviceCategoryListSerializer(serializers.HyperlinkedModelSerializer):

    manufacturers = fields.SerializerMethodField()

    class Meta:
        model = DeviceCategory
        fields = ['id', 'name', 'photo', 'url', 'manufacturers']
        extra_kwargs = {
            'url': {'view_name': 'api:devicecategory-detail'},
        }

    @extend_schema_field(OpenApiTypes.URI)
    def get_manufacturers(self, obj) -> str:
        return reverse('api:devicecategory-manufacturers', [obj.pk], request=self.context['request'])


class DeviceCategoryInstSerializer(serializers.HyperlinkedModelSerializer):

    manufacturers = fields.SerializerMethodField()

    class Meta:
        model = DeviceCategory
        fields = ['id', 'name', 'photo', 'url', 'device', 'manufacturers']
        extra_kwargs = {
            'url': {'view_name': 'api:devicecategory-detail'},
            'device': {'view_name': 'api:manufacturer-detail'},
        }

    @extend_schema_field(OpenApiTypes.URI)
    def get_manufacturers(self, obj) -> str:
        return reverse('api:devicecategory-manufacturers', [obj.pk], request=self.context['request'])


class ManufacturerListSerializer(serializers.HyperlinkedModelSerializer):

    models = fields.SerializerMethodField()

    class Meta:
        model = Manufacturer
        fields = ['id', 'device_category', 'name', 'photo', 'url', 'models']
        extra_kwargs = {
            'url': {'view_name': 'api:manufacturer-detail'},
            'device_category': {'view_name': 'api:devicecategory-detail'},
        }

    @extend_schema_field(OpenApiTypes.URI)
    def get_models(self, obj) -> str:
        return reverse('api:manufacturer-models', [obj.pk], request=self.context['request'])


class ManufacturerInstSerializer(serializers.HyperlinkedModelSerializer):

    models = fields.SerializerMethodField()

    class Meta:
        model = Manufacturer
        fields = ['id', 'device_category', 'name', 'photo', 'url', 'modelstemplate', 'models']
        extra_kwargs = {
            'url': {'view_name': 'api:manufacturer-detail'},
            'device_category': {'view_name': 'api:devicecategory-detail'},
            'modelstemplate': {'view_name': 'api:modelstemplate-detail'},
        }

    @extend_schema_field(OpenApiTypes.URI)
    def get_models(self, obj) -> str:
        return reverse('api:manufacturer-models', [obj.pk], request=self.context['request'])


class ModelsTemplateListSerializer(serializers.HyperlinkedModelSerializer):

    templates = fields.SerializerMethodField()

    class Meta:
        model = ModelsTemplate
        fields = ['id', 'manufacturer', 'name', 'url', 'template_set', 'templates']
        extra_kwargs = {
            'url': {'view_name': 'api:modelstemplate-detail'},
            'manufacturer': {'view_name': 'api:manufacturer-detail'},
            'template_set': {'view_name': 'api:template-detail'}
        }

    @extend_schema_field(OpenApiTypes.URI)
    def get_templates(self, obj) -> str:
        return reverse('api:modelstemplate-templates', [obj.pk], request=self.context['request'])
