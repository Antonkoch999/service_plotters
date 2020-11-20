from rest_framework import fields, serializers
from main_service_of_plotters.apps.materials.models import Template, Label


class TemplateListSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Template
        fields = ['id', 'name', 'file_photo', 'file_plt', 'size', 'url']
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


class TemplateBlueprintOnlySerializer(serializers.HyperlinkedModelSerializer):

    file = fields.SerializerMethodField('get_file')

    def get_file(self, obj) -> str:
        return self.context['request'].build_absolute_uri(obj.file_plt.url)

    class Meta:

        model = Template
        fields = ['file']
