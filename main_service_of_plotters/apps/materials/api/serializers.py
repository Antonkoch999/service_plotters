"""App models serializers."""

from rest_framework import fields, serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes

from main_service_of_plotters.apps.materials.models import Template, Label


class TemplateListSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer of template when method is `list`."""

    class Meta:
        """Metadata of serializer."""

        model = Template
        fields = ['id', 'name', 'file_photo', 'file_plt', 'size', 'url']
        extra_kwargs = {
            'url': {
                'view_name': 'api:template-detail'
            },
        }


class LabelListSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer of template when method is `retrieve`."""

    class Meta:
        """Metadata of serializer."""

        model = Label
        fields = ['id', 'scratch_code', 'barcode', 'count', 'dealer',
                  'user', 'is_active', 'url']
        extra_kwargs = {
            'url': {'view_name': 'api:label-detail', },
            'dealer': {'view_name': 'api:user-detail', },
            'user': {'view_name': 'api:user-detail'},
        }


class TemplateBlueprintOnlySerializer(serializers.HyperlinkedModelSerializer):
    """Serializer of model with only one field - link to plt file."""

    file = fields.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.URI)
    def get_file(self, obj) -> str:
        """Return url to file."""
        return self.context['request'].build_absolute_uri(obj.file_plt.url)

    class Meta:
        """Metadata of serializer."""

        model = Template
        fields = ['file']
