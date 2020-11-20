"""Statistics classes serializers for api."""

from rest_framework import serializers
from main_service_of_plotters.apps.statistics.models import (
    StatisticsPlotter, StatisticsTemplate, CuttingTransaction)


class StatisticsPlotterListSerializer(serializers.HyperlinkedModelSerializer):
    """Serializing statistics plotter instance for api views."""

    class Meta:
        """Metadata of Statistics Plotter."""

        model = StatisticsPlotter
        fields = ['id', 'plotter', 'ip', 'last_request', 'count_cut']
        extra_kwargs = {
            'plotter': {'view_name': 'api:plotter-detail'},
        }


class StatisticsTemplateListSerializer(serializers.HyperlinkedModelSerializer):
    """Serializing statistics template instance for api views."""

    class Meta:
        """Metadata of Statistics Template."""

        model = StatisticsTemplate
        fields = ['id', 'plotter', 'template', 'count']
        extra_kwargs = {
            'plotter': {'view_name': 'api:plotter-detail'},
            'template': {'view_name': 'api:template-detail'}
        }


class CuttingTransactionListSerializer(serializers.HyperlinkedModelSerializer):
    """Serializing cutting transaction instance for api views."""

    class Meta:
        """Metadata of Cutting Transaction."""

        model = CuttingTransaction
        fields = ['id', 'user', 'plotter', 'template', 'date_cutted']
        extra_kwargs = {
            'user': {'view_name': 'api:user-detail'},
            'plotter': {'view_name': 'api:plotter-detail'},
            'template': {'view_name': 'api:template-detail'},
        }
