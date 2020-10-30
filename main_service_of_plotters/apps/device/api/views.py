from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import permission_classes
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated

from .serializers import PlotterSerializer, AdministratorPlotterSerializer, \
    DealerPlotterSerializer, UserPlotterSerializer
from ..models import Plotter
from .permissions import PlotterUserPermission


# TODO Process with permission
@permission_classes([IsAuthenticated, DjangoModelPermissions, PlotterUserPermission])
class PlotterViewSet(ModelViewSet):
    """Create, update, list, retriev views of plotter."""

    serializer_class = PlotterSerializer
    queryset = Plotter.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        # Plotter can see only owned plotters
        if self.request.user.is_dealer():
            queryset = queryset.filter(dealer=self.request.user)
        # User can see only owned plotters
        if self.request.user.is_user():
            queryset = queryset.filter(user=self.request.user)

        return queryset

    def get_serializer_class(self):
        if self.request.user.is_dealer():
            return DealerPlotterSerializer
        if self.request.user.is_user():
            return UserPlotterSerializer
        if self.request.user.is_administrator():
            return AdministatorPlotterSerializer
        return super().get_serializer_class()
