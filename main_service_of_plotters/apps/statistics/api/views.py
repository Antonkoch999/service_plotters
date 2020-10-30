from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.viewsets import ModelViewSet

from main_service_of_plotters.apps.statistics.models import (
    StatisticsPlotter, StatisticsTemplate, CuttingTransaction)
from .serializers import (
    StatisticsPlotterListSerializer, StatisticsTemplateListSerializer,
    CuttingTransactionListSerializer)
from .filters import IsUserPlotterOwnFilter, IsDealerPlotterOwnFilter


@permission_classes([IsAuthenticated, DjangoModelPermissions])
class StatisticsPlotterViewSet(ModelViewSet):
    serializer_class = StatisticsPlotterListSerializer
    queryset = StatisticsPlotter.objects.all()
    filter_backends = (IsUserPlotterOwnFilter, IsDealerPlotterOwnFilter)


@permission_classes([IsAuthenticated, DjangoModelPermissions])
class StatisticsTemplateViewSet(ModelViewSet):
    serializer_class = StatisticsTemplateListSerializer
    queryset = StatisticsTemplate.objects.all()


@permission_classes([IsAuthenticated, DjangoModelPermissions])
class CuttingTransactionViewSet(ModelViewSet):
    serializer_class = CuttingTransactionListSerializer
    queryset = CuttingTransaction.objects.all()
