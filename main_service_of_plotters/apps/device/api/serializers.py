"""Device classes serializers for api."""

from rest_framework import serializers

from ..models import Plotter


class AdministratorPlotterSerializer(serializers.HyperlinkedModelSerializer):
    """Serializing Plotter instance for api views."""

    class Meta:
        model = Plotter
        fields = ['serial_number', 'available_film', 'user', 'dealer', 'url']
        extra_kwargs = {
            'url': {'view_name': 'api:plotter-detail', },
            'user': {'view_name': 'api:user-detail', },
            'dealer': {'view_name': 'api:user-detail', },
        }


class DealerPlotterSerializer(serializers.HyperlinkedModelSerializer):
    """Serializing Plotter instance for api views."""

    class Meta:
        model = Plotter
        fields = ['serial_number', 'available_film', 'user', 'url']
        extra_kwargs = {
            'url': {'view_name': 'api:plotter-detail', },
            'user': {'view_name': 'api:user-detail', },
            'dealer': {'view_name': 'api:user-detail', },
        }
        read_only_fields = ('serial_number', )


class UserPlotterSerializer(serializers.HyperlinkedModelSerializer):
    """Serializing Plotter instance for api views."""

    class Meta:
        model = Plotter
        fields = ['serial_number', 'available_film', 'url']
        extra_kwargs = {
            'url': {'view_name': 'api:plotter-detail', },
            'user': {'view_name': 'api:user-detail', },
            'dealer': {'view_name': 'api:user-detail', },
        }
        read_only_fields = ('serial_number', 'available_film')


class PlotterSerializer(serializers.HyperlinkedModelSerializer):
    """Serializing Plotter instance for api views."""

    class Meta:
        model = Plotter
        fields = ['serial_number', 'available_film', 'user', 'dealer', 'url']
        extra_kwargs = {
            'url': {'view_name': 'api:plotter-detail', },
            'user': {'view_name': 'api:user-detail', },
            'dealer': {'view_name': 'api:user-detail', },
        }
