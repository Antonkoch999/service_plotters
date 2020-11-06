from django.contrib import admin
from django.db.models import Q

from .models import Ticket, PopularProblem
from .forms import TechSpecialistForm
from main_service_of_plotters.apps.users.models import User


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['header', 'status', 'reporter', 'assignee']

    def get_form(self, request, obj=None, **kwargs):

        if request.user.groups.filter(name='Technical_Specialist').exists():
            kwargs['form'] = TechSpecialistForm
            form = super().get_form(request, obj, **kwargs)
            form.base_fields['assignee'].queryset = User.objects.filter(
                id=request.user.pk)
            return form
        return super().get_form(request, obj, **kwargs)

    def get_list_display(self, request):

        list_display = ['header', 'status', 'assignee']
        # If user is `Dealer` or User
        if request.user.groups.filter(name='Technical_Specialist').exists():
            # without `scretch code`
            list_display = ['header', 'status', 'assignee']
        return list_display

    def get_queryset(self, request):

        qs = super().get_queryset(request)
        if request.user.groups.filter(name='Technical_Specialist').exists():
            qs = qs.filter(Q(status='O') | Q(assignee=request.user.pk))
        return qs

    def get_list_filter(self, request):
        """Add filters on list page depeded of logged user."""

        filters = ('status', )
        if request.user.groups.filter(name='Technical_Specialist').exists():
            filters = ('status',)
        return filters


@admin.register(PopularProblem)
class PopularProblemAdmin(admin.ModelAdmin):
    pass
