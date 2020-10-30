from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import permission_classes
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
import rest_framework.status as status
from rest_framework.response import Response

from .serializers import PlotterSerializer
from ..models import Plotter
from .permissions import PlotterUserPermission
from .filters import IsUserOwnFilter, IsDealerOwnFilter
from main_service_of_plotters.apps.materials.models import Template
from main_service_of_plotters.apps.statistics.models import CuttingTransaction, StatisticsPlotter, StatisticsTemplate


@permission_classes([IsAuthenticated, DjangoModelPermissions, PlotterUserPermission])
class PlotterViewSet(ModelViewSet):
    """Create, update, list, retriev views of plotter."""

    serializer_class = PlotterSerializer
    queryset = Plotter.objects.all()
    filter_backends = (IsUserOwnFilter, IsDealerOwnFilter)


# Actions with cutting
@api_view(['POST'])
def cut(request):
    template_pk = request.data.get('template')
    plotter_pk = request.data.get('plotter')
    template = get_object_or_404(Template, pk=template_pk)
    plotter = get_object_or_404(Plotter, pk=plotter_pk)
    if plotter.available_film < 0:
        return Response(data='Available films is over', status=status.HTTP_403_FORBIDDEN)
    # TODO Check plotter ip with client ip
    plotter.available_film -= 1
    StatisticsPlotter.objects.create(
        plotter=plotter,
        ip=request.META['REMOTE_ADDR'],
        count_cut=1
    )
    StatisticsTemplate.objects.create(
        plotter=plotter,
        template=template,
        count=1
    )
    CuttingTransaction.objects.create(
        user=request.user,
        plotter=plotter,
        template=template,
    )
    with open(template.file_plt, 'r') as f:
        file_data = f.read

    response = Response(file_data, content_type='application/octet-stream')
    response['Content-Disposition'] = 'attachment; filename="blueprint.plt"'
    return Response
