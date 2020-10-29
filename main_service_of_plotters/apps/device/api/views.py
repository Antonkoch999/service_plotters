from rest_framework.mixins import ListModelMixin, \
    RetrieveModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet

from .serializers import PlotterSerializer
from ..models import Plotter


class PlotterViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, CreateModelMixin, GenericViewSet):
    serializer_class = PlotterSerializer
    queryset = Plotter.objects.all()
