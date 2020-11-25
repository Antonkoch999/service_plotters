"""This module create forms."""

from django import forms

from main_service_of_plotters.apps.device.models import Plotter
from main_service_of_plotters.apps.materials.models import Label


class PlotterForm(forms.ModelForm):
    """This class create form for model Plotter."""

    class Meta:
        """Metadata of Plotter."""

        model = Plotter
        fields = ('dealer', 'user', 'serial_number', 'date_creation')


class DealerPlotterForm(PlotterForm):
    """This class excludes field 'dealer' from model Plotter."""

    class Meta:
        """Metadata of Plotter."""

        fields = ('user', 'serial_number',)


class AdministratorPlotterForm(PlotterForm):
    """This class excludes field 'user' from model Plotter."""

    class Meta:
        """Metadata of Plotter."""

        fields = ('dealer', 'serial_number', )


class UserPlotterForm(PlotterForm):
    """This class excludes field 'user' from model Plotter."""

    class Meta:
        """Metadata of Plotter."""

        fields = ('serial_number', )


class AddLabelForm(forms.Form):
    """This class create form for model Label."""
    scratch_code = forms.CharField(max_length=16)
    # class Meta:
    #     """Metadata of Label."""
    #
    #     model = Label
    #     fields = ('scratch_code', )
