from django.contrib import admin
from django.db.models import Q
from django.utils.translation import gettext as _
from django.http import HttpResponseRedirect
from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required

from .models import Ticket, PopularProblem
from .forms import TechSpecialistForm, UserForm
from main_service_of_plotters.apps.users.models import User

@staff_member_required
def user_add_ticket(request):
    return HttpResponseRedirect('ticket:user_add_ticket')

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['header', 'status', 'reporter', 'assignee']
    change_form_template = 'ticket/admin_change_form.html'
    change_list_template = 'admin/change_list_ticket.html'

    def get_form(self, request, obj=None, **kwargs):

        if request.user.groups.filter(name='Technical_Specialist').exists():
            kwargs['form'] = TechSpecialistForm
            form = super().get_form(request, obj, **kwargs)
            form.base_fields['assignee'].queryset = User.objects.filter(
                id=request.user.pk)
            return form
        elif request.user.groups.filter(name='User').exists():
            kwargs['form'] = UserForm
            form = super().get_form(request, obj, **kwargs)
            return form
        return super().get_form(request, obj, **kwargs)

    def get_list_display(self, request):

        list_display = ['header', 'assignee', 'reporter', 'status']
        # If user is `Dealer` or User
        if request.user.groups.filter(name='Technical_Specialist').exists():
            # without `scretch code`
            list_display = ['header', 'status', 'assignee']

        return list_display

    def get_queryset(self, request):

        qs = super().get_queryset(request)
        if request.user.groups.filter(name='Technical_Specialist').exists():
            qs = qs.filter(Q(status='O') | Q(assignee=request.user.pk))
        elif request.user.groups.filter(name='User').exists():
            qs = qs.filter(reporter=request.user.pk)
        return qs

    def get_list_filter(self, request):
        """Add filters on list page depeded of logged user."""

        filters = ('status', )
        if request.user.groups.filter(name='Technical_Specialist').exists():
            filters = ('status',)
        return filters

    def response_change(self, request, obj):
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
                    self.message_user(request,
                                      f'{obj} {_("changes status to ")}{obj.status.label}')
                return HttpResponseRedirect('.')
            elif request.user.groups.filter(name='Technical_Specialist').exists():
                obj.assignee = request.user
                obj.status = Ticket.status_variants.IN_WORK
                obj.save()
                self.message_user(request,
                                  f'{obj}{_("Change status to")}{obj.status.label}')
                return HttpResponseRedirect('.')
        return super().response_change(request, obj)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('user-add-tikcet/', user_add_ticket, name='user_add_ticket'),
        ]
        return urls + my_urls





@admin.register(PopularProblem)
class PopularProblemAdmin(admin.ModelAdmin):
    pass
