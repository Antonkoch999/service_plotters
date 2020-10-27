"""This module create forms."""

from django import forms

from main_service_of_plotters.apps.device.models import Plotter
from main_service_of_plotters.apps.materials.models import Label


class PlotterForm(forms.ModelForm):
    """This class create form for model Plotter."""

    class Meta:
        model = Plotter
        fields = ('dealer', 'user', 'serial_number', 'available_film')


class DealerPlotterForm(PlotterForm):
    """This class excludes field 'dealer' from model Plotter."""

    class Meta:
        exclude = ('dealer', )


class AdministratorPlotterForm(PlotterForm):
    """This class excludes field 'user' from model Plotter."""

    class Meta:
        exclude = ('user', )


class AddLabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ('scratch_code', )
