from django.utils.translation import ugettext_lazy as _
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.decorators import permission_classes
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.decorators import api_view
import rest_framework.status as status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

from .serializers import PlotterSerializer, CutSerializer, AddLabelSerializer
from ..models import Plotter
from .permissions import PlotterUserPermission
from .filters import IsUserOwnFilter, IsDealerOwnFilter
from main_service_of_plotters.apps.statistics.models import CuttingTransaction, StatisticsPlotter, StatisticsTemplate
from main_service_of_plotters.apps.materials.api.serializers import TemplateBlueprintOnlySerializer
from main_service_of_plotters.apps.materials.models import Label


@permission_classes([IsAuthenticated, DjangoModelPermissions, PlotterUserPermission])
class PlotterViewSet(ModelViewSet):
    """Create, update, list, retriev views of plotter."""

    serializer_class = PlotterSerializer
    queryset = Plotter.objects.all()
    filter_backends = (IsUserOwnFilter, IsDealerOwnFilter)


class PlotterViewSetByDID(RetrieveModelMixin, GenericViewSet):

    serializer_class = PlotterSerializer
    queryset = Plotter.objects.all()

    lookup_field = 'device_id'


class PlotterViewSetBySN(RetrieveModelMixin, GenericViewSet):

    serializer_class = PlotterSerializer
    queryset = Plotter.objects.all()
    lookup_field = 'serial_number'


# Actions with cutting
@api_view(['POST'])
def cut(request):
    serializer = CutSerializer(data=request.data)
    if serializer.is_valid():
        print(serializer.validated_data)
        plotter = serializer.validated_data['plotter']
        template = serializer.validated_data['template']
        if plotter.available_films <= 0:
            return Response(data=_('Available films is over'),
                            status=status.HTTP_403_FORBIDDEN)
        # TODO Check plotter ip with client ip
        label = plotter.first_linked_label
        label.available_count -= 1
        label.save()
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
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def scratch_code(request):
    serializer = AddLabelSerializer(data=request.data)
    if serializer.is_valid():
        print(serializer.validated_data)
        plotter = serializer.validated_data['plotter']
        scratch_code = serializer.validated_data['scratch_code']
        try:
            label = Label.objects.filter(is_active=False).get(
                scratch_code=scratch_code)
        except ObjectDoesNotExist:
            messages.add_message(request, messages.ERROR,
                                 'Scratch code not found')
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            plotter.link_label(label)
            return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
