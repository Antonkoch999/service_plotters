from rest_framework import serializers
from main_service_of_plotters.apps.materials.models import Template, Label


class TemplateListSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Template
        fields = ['id', 'name', 'file_photo', 'file_plt', 'url']
        extra_kwargs = {
            'url': {
                'view_name': 'api:template-detail'
            },
        }


class LabelListSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Label
        fields = ['id', 'scratch_code', 'barcode', 'count', 'dealer',
                  'user', 'is_active', 'url']
        extra_kwargs = {
            'url': {'view_name': 'api:label-detail', },
            'dealer': {'view_name': 'api:user-detail', },
            'user': {'view_name': 'api:user-detail'},
        }

