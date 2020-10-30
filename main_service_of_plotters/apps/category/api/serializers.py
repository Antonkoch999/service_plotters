from rest_framework import serializers
from main_service_of_plotters.apps.category.models import (
    DeviceCategory, Manufacturer, ModelsTemplate)


class DeviceCategoryListSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = DeviceCategory
        fields = ['id', 'name', 'photo', 'url', 'device']
        extra_kwargs = {
            'url': {'view_name': 'api:devicecategory-detail'},
            'device': {'view_name': 'api:manufacturer-detail'},
        }


class ManufacturerListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ['id', 'device_category', 'name', 'photo', 'url']
        extra_kwargs = {
            'url': {'view_name': 'api:manufacturer-detail'},
            'device_category': {'view_name': 'api:devicecategory-detail'},
        }


class ModelsTemplateListSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ModelsTemplate
        fields = ['id', 'manufacturer', 'name', 'url']
        extra_kwargs = {
            'url': {'view_name': 'api:modelstemplate-detail'},
            'manufacturer': {'view_name': 'api:manufacturer-detail'},
        }
