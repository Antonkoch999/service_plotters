from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import permission_classes
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.decorators import api_view
import rest_framework.status as status
from rest_framework.response import Response
from django.http import HttpResponseRedirect

from .serializers import PlotterSerializer, CutSerializer
from ..models import Plotter
from .permissions import PlotterUserPermission
from .filters import IsUserOwnFilter, IsDealerOwnFilter
from main_service_of_plotters.apps.statistics.models import CuttingTransaction, StatisticsPlotter, StatisticsTemplate
from main_service_of_plotters.apps.materials.api.serializers import TemplateBlueprintOnlySerializer


@permission_classes([IsAuthenticated, DjangoModelPermissions, PlotterUserPermission])
class PlotterViewSet(ModelViewSet):
    """Create, update, list, retriev views of plotter."""

    serializer_class = PlotterSerializer
    queryset = Plotter.objects.all()
    filter_backends = (IsUserOwnFilter, IsDealerOwnFilter)


# Actions with cutting
@api_view(['POST'])
def cut(request):
    serializer = CutSerializer(data=request.data)
    if serializer.is_valid():
        print(serializer.validated_data)
        plotter = serializer.validated_data['plotter']
        template = serializer.validated_data['template']
        if plotter.available_film <= 0:
            return Response(data='Available films is over', status=status.HTTP_403_FORBIDDEN)
        # TODO Check plotter ip with client ip
        plotter.available_film -= 1
        plotter.save()
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

        seria = TemplateBlueprintOnlySerializer(template,
                                                context={'request': request})
        return Response(seria.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
