from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import permission_classes
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated

from .serializers import PlotterSerializer
from ..models import Plotter
from .permissions import PlotterUserPermission
from .filters import IsUserOwnFilter, IsDealerOwnFilter


# TODO Process with permission
@permission_classes([IsAuthenticated, DjangoModelPermissions, PlotterUserPermission])
class PlotterViewSet(ModelViewSet):
    """Create, update, list, retriev views of plotter."""

    serializer_class = PlotterSerializer
    queryset = Plotter.objects.all()
    filter_backends = (IsUserOwnFilter, IsDealerOwnFilter)

    # def get_serializer_class(self):
    #     if self.request.user.is_dealer():
    #         return DealerPlotterSerializer
    #     if self.request.user.is_user():
    #         return UserPlotterSerializer
    #     if self.request.user.is_administrator():
    #         return AdministratorPlotterSerializer
    #     return super().get_serializer_class()
