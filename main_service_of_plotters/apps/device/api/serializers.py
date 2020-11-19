"""Device classes serializers for api."""

from rest_framework import serializers

from ..models import Plotter
from main_service_of_plotters.apps.materials.models import Template, Label


class PlotterSerializer(serializers.HyperlinkedModelSerializer):
    """Serializing Plotter instance for api views."""

    class Meta:
        model = Plotter
        fields = ['id', 'serial_number', 'available_film', 'user', 'dealer', 'url', 'cut_amount']
        extra_kwargs = {
            'url': {'view_name': 'api:plotter-detail', },
            'user': {'view_name': 'api:user-detail', },
            'dealer': {'view_name': 'api:user-detail', },
        }

    def __init__(self, *args, **kwargs):

        # TODO Rewrite this crap

        get_inst = False
        if len(args) > 0 and isinstance(args[0], Plotter):
            plotter = args[0]
            get_inst = True
            user_presented = plotter.user is not None
            dealer_presented = plotter.dealer is not None

        user = kwargs.get('context', {}).get('request').user

        super().__init__(*args, **kwargs)

        if user.is_user():
            self.fields.pop('user')
        elif user.is_dealer():
            self.fields.pop('dealer')
            if get_inst and user_presented:
                self.fields.get('user').read_only = True
        elif user.is_administrator():
            self.fields.get('user').read_only = True
            if get_inst and dealer_presented:
                self.fields.get('dealer').read_only = True


class CutSerializer(serializers.Serializer):
    plotter = serializers.PrimaryKeyRelatedField(queryset=Plotter.objects.all())
    template = serializers.PrimaryKeyRelatedField(queryset=Template.objects.all())


class AddLabelSerializer(serializers.Serializer):
    plotter = serializers.PrimaryKeyRelatedField(queryset=Plotter.objects.all())
    scratch_code = serializers.CharField(max_length=16)
