"""Device classes serializers for api."""

from rest_framework import serializers

from ..models import Plotter


class PlotterSerializer(serializers.HyperlinkedModelSerializer):
    """Serializing Plotter instance for api views."""
    class Meta:
        model = Plotter
        # ISSUE: maybe worth to add fields `dealer` `user`?
        fields = ['serial_number', 'available_film', 'url']
        extra_kwargs = {
            'url': {
                'view_name': 'api:plotter-detail'
            }
        }
