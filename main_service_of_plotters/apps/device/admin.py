"""This class is representation of device in the admin interface."""

from django.contrib import admin

from main_service_of_plotters.apps.device.models import Plotter
from main_service_of_plotters.apps.users.models import User

from .forms import AdministratorPlotterForm, DealerPlotterForm, PlotterForm


class PlotterAdmin(admin.ModelAdmin):
    """Class is representation of a model Plotter in the admin interface."""

    form = PlotterForm
    list_display = ('serial_number', 'dealer', 'user', )

    def get_form(self, request, obj=None, **kwargs):
        """"Changes form class depending on the user role."""

        if request.user.role == 'Dealer':
            kwargs['form'] = DealerPlotterForm
            form = super().get_form(request, obj, **kwargs)
            form.base_fields['user'].queryset = User.objects.filter(
                dealer_id=request.user.pk)
            return form
        elif request.user.role == 'Administrator':
            kwargs['form'] = AdministratorPlotterForm
        return super().get_form(request, obj, **kwargs)

    def get_queryset(self, request):
        """Changes QuerySet model instance depending of the user groups."""

        qs = super().get_queryset(request)
        if request.user.groups.filter(name='Dealer').exists():
            return qs.filter(dealer=request.user.pk)
        elif request.user.groups.filter(name='User').exists():
            return qs.filter(user=request.user.pk)
        return qs


admin.site.register(Plotter, PlotterAdmin)
