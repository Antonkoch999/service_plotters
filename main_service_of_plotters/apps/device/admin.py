"""This class is representation of device in the admin interface."""

from django.conf.urls import url
from django.contrib import admin, messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from import_export import resources
from import_export.admin import ImportExportMixin

from main_service_of_plotters.apps.device.models import Plotter
from main_service_of_plotters.apps.materials.models import Label
from main_service_of_plotters.apps.users.models import User
from .forms import AdministratorPlotterForm, DealerPlotterForm, PlotterForm, \
    AddLabelForm, UserPlotterForm


class PlotterResource(resources.ModelResource):
    """Model Resourse for django-import-export."""

    class Meta:
        model = Plotter


class PlotterAdmin(ImportExportMixin, admin.ModelAdmin):
    """Class is representation of a model Plotter in the admin interface."""
    resource_class = PlotterResource
    form = PlotterForm
    list_display = ('serial_number', 'dealer', 'user', 'available_films',
                    'account_actions', )
    change_list_template = "admin/import_export/plotter_change_list.html"

    def get_form(self, request, obj=None, **kwargs):
        """Changes form class depending on the user role."""

        if request.user.role == 'Dealer':
            kwargs['form'] = DealerPlotterForm
            form = super().get_form(request, obj, **kwargs)
            form.base_fields['user'].queryset = User.objects.filter(
                dealer=request.user)
        elif request.user.role == 'Administrator':
            kwargs['form'] = AdministratorPlotterForm
        elif request.user.role == 'User':
            kwargs['form'] = UserPlotterForm
        return super().get_form(request, obj, **kwargs)

    def get_queryset(self, request):
        """Changes QuerySet model instance depending of the user groups."""

        qs = super().get_queryset(request)
        if request.user.groups.filter(name='Dealer').exists():
            qs = qs.filter(dealer=request.user.pk)
        elif request.user.groups.filter(name='User').exists():
            qs = qs.filter(user=request.user.pk)
        return qs

    def get_list_display(self, request):
        """Change list_display list depended of logged user."""

        # If user is `Dealer` or User
        if request.user.groups.filter(name='Dealer').exists():
            # without `scretch code`
            return ['serial_number', 'dealer', 'user', 'available_films']
        return super().get_list_display(request)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                r'^(?P<plotter_id>.+)/addlabel/$',
                self.admin_site.admin_view(self.process_label),
                name='add_label',
            ),
        ]
        return custom_urls + urls

    def account_actions(self, obj):
        return format_html(
            ''.join(['<a class="button" href="{}">',
                    str(_('Add label')),
                    '</a>&nbsp;']),
            reverse('admin:add_label', args=[obj.pk]),

        )
    account_actions.short_description = _('Account Actions')
    account_actions.allow_tags = True

    def process_label(self, request, plotter_id):
        plotter = Plotter.objects.get(pk=plotter_id)
        if request.method == 'POST':
            form = AddLabelForm(request.POST)
            if form.is_valid():
                try:
                    label = Label.objects.filter(
                        is_active=False).get(
                        scratch_code=form.cleaned_data['scratch_code'])
                    if not (label.dealer == plotter.dealer or
                            label.user == plotter.user):
                        raise ObjectDoesNotExist
                except ObjectDoesNotExist:
                    messages.add_message(request, messages.ERROR,
                                         _('Scratch code not found'))
                    return HttpResponseRedirect('./')
                plotter.link_label(label)

            return HttpResponseRedirect('../..')
        else:
            form = AddLabelForm()
        return render(request, 'admin/adding_label.html', {'form': form})


admin.site.register(Plotter, PlotterAdmin)
