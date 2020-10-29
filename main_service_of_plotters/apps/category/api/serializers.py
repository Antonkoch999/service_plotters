from rest_framework import serializers
from main_service_of_plotters.apps.category.models import (
    DeviceCategory, Manufacturer, ModelsTemplate)


class DeviceCategoryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeviceCategory
        fields = ['id', 'name', 'photo']


class ManufacturerListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ['id', 'device_category', 'name', 'photo']
        extra_kwargs = {
            'device_category': {
                'view_name': 'api:devicecategory-detail'
            },
        }


class ModelsTemplateListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ModelsTemplate
        fields = ['id', 'manufacturer', 'name']
        extra_kwargs = {
            'manufacturer': {
                'view_name': 'api:manufacturer-detail'
            },
        }
