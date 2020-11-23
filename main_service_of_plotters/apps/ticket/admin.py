"""This class is representation of tickets in the admin interface."""

from django.contrib import admin
from django.db.models import Q
from django.utils.translation import gettext as _
from django.http import HttpResponseRedirect

from main_service_of_plotters.apps.users.models import User
from .models import Ticket, PopularProblem
from .forms import TechSpecialistForm, UserForm


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    """Class representation of model Ticket in interface admin."""

    change_form_template = 'ticket/admin_change_form.html'
    change_list_template = 'admin/change_list_ticket.html'

    def get_form(self, request, obj=None, **kwargs):
        """Change form class depending on the user groups."""
        if request.user.groups.filter(name='Technical_Specialist').exists():
            kwargs['form'] = TechSpecialistForm
            form = super().get_form(request, obj, **kwargs)
            form.base_fields['assignee'].queryset = User.objects.filter(
                id=request.user.pk)
        elif request.user.groups.filter(name='User').exists():
            kwargs['form'] = UserForm
        return super().get_form(request, obj, **kwargs)

    def get_list_display(self, request):
        """Change list_display list depended of user groups."""
        list_display = ['header', 'assignee', 'reporter', 'status']
        # If user is `Dealer` or User
        if request.user.groups.filter(name='Technical_Specialist').exists():
            # without `scretch code`
            list_display = ['header', 'status', 'assignee']
        return list_display

    def get_queryset(self, request):
        """Change queryset list depended of user groups."""
        qs = super().get_queryset(request)
        if request.user.groups.filter(name='Technical_Specialist').exists():
            qs = qs.filter(Q(status='O') | Q(assignee=request.user.pk))
        elif request.user.groups.filter(name='User').exists():
            qs = qs.filter(reporter=request.user.pk)
        return qs

    def get_list_filter(self, request):
        """Add filters on list page depended of logged user."""
        filters = ('status', )
        if request.user.groups.filter(name='Technical_Specialist').exists():
            filters = ('status', )
        return filters

    def response_change(self, request, obj):
        """Create custom button in change form."""
        # TODO user must have change permission to close ticket but this is not propper condition
        # Rethink it
        if '_make_close' in request.POST:
            if request.user.groups.filter(name='User').exists():
                if obj.reporter != request.user:
                    self.message_user(request, _(
                        'You dont have permission to close this ticket'))
                else:
                    obj.status = Ticket.status_variants.CLOSED
                    obj.save()
                    self.message_user(
                        request,
                        f'{obj} {_("changes status to ")}{obj.status.label}')
                return HttpResponseRedirect('.')
            elif request.user.groups.filter(name='Technical_Specialist').exists():
                obj.assignee = request.user
                obj.status = Ticket.status_variants.IN_WORK
                obj.save()
                self.message_user(
                    request,
                    f'{obj}{_("Change status to")}{obj.status.label}')
                return HttpResponseRedirect('.')
        return super().response_change(request, obj)


@admin.register(PopularProblem)
class PopularProblemAdmin(admin.ModelAdmin):
    """Class representation of model Popular Problem in interface admin."""
