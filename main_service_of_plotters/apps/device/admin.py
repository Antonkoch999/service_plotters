from django.contrib import admin
from django import forms

from main_service_of_plotters.apps.device.models import Plotter
from main_service_of_plotters.apps.users.models import User


class PlotterForm(forms.ModelForm):
    class Meta:
        model = Plotter
        fields = ('dealer', 'user', 'serial_number', )


class DealerPlotterForm(PlotterForm):
    class Meta:
        exclude = ('dealer', )


class AdministratorPlotterForm(PlotterForm):
    class Meta:
        exclude = ('user', )


class PlotterAdmin(admin.ModelAdmin):
    form = PlotterForm
    list_display = ('serial_number', 'dealer', 'user', )

    def get_form(self, request, obj=None, **kwargs):
        if request.user.role == 'Dealer':
            kwargs['form'] = DealerPlotterForm
            form = super().get_form(request, obj, **kwargs)
            form.base_fields['user'].queryset = User.objects.filter(dealer_id=request.user.pk)
            return form
        elif request.user.role == 'Administrator':
            kwargs['form'] = AdministratorPlotterForm
        return super().get_form(request, obj, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.filter(name='Dealer').exists():
            return qs.filter(dealer=request.user.pk)
        elif request.user.groups.filter(name='User').exists():
            return qs.filter(user=request.user.pk)
        return qs


admin.site.register(Plotter, PlotterAdmin)

