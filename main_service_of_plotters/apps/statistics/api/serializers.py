from rest_framework import serializers
from main_service_of_plotters.apps.statistics.models import (
    StatisticsPlotter, StatisticsTemplate, CuttingTransaction)


class StatisticsPlotterListSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = StatisticsPlotter
        fields = ['id', 'plotter', 'ip', 'last_request', 'count_cut']
        extra_kwargs = {
            'plotter': {'view_name': 'api:plotter-detail'},
        }


class StatisticsTemplateListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StatisticsTemplate
        fields = ['id', 'plotter', 'template', 'count']
        extra_kwargs = {
            'plotter': {'view_name': 'api:plotter-detail'},
            'template': {'view_name': 'api:template-detail'}
        }


class CuttingTransactionListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CuttingTransaction
        fields = ['id', 'user', 'plotter', 'template', 'date_cutted']
        extra_kwargs = {
            'user': {'view_name': 'api:user-detail'},
            'plotter': {'view_name': 'api:plotter-detail'},
            'template': {'view_name': 'api:template-detail'},
        }
