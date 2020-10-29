from main_service_of_plotters.apps.statistics.models import (
    StatisticsPlotter, StatisticsTemplate, CuttingTransaction)
from rest_framework.viewsets import ModelViewSet
from .serializers import (
    StatisticsPlotterListSerializer, StatisticsTemplateListSerializer,
    CuttingTransactionListSerializer)
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password


class StatisticsPlotterViewSet(ModelViewSet):
    serializer_class = StatisticsPlotterListSerializer
    queryset = StatisticsPlotter.objects.all()


class StatisticsTemplateViewSet(ModelViewSet):
    serializer_class = StatisticsTemplateListSerializer
    queryset = StatisticsTemplate.objects.all()


class CuttingTransactionViewSet(ModelViewSet):
    serializer_class = CuttingTransactionListSerializer
    queryset = CuttingTransaction.objects.all()
