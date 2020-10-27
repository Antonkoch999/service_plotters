"""This class is representation of users in the admin interface."""

from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from main_service_of_plotters.apps.users import forms, models


class UserAdmin(BaseUserAdmin):
    """Class is representation of a model User in the admin interface."""

    form = forms.UserChangeForm
    add_form = forms.UserCreationForm
    list_display = ('username', 'email', 'role', 'dealer_id')
    list_filter = ('role',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'first_name', 'last_name',
                           'role', 'is_active',
                           )
                }
         ),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'role', 'password1',
                       'password2',
                       ),
        }),
    )
    search_fields = ('role',)

    def get_form(self, request, obj=None, **kwargs):
        """Changes form class depending on the user role."""

        if request.user.role == 'Dealer':
            kwargs['form'] = forms.DealerUserForm
        elif request.user.role == 'Administrator':
            kwargs['form'] = forms.AdministratorUserForm
        return super().get_form(request, obj, **kwargs)

    def get_queryset(self, request):
        """Changes QuerySet model instance depending of the user groups."""

        qs = super().get_queryset(request)
        if request.user.groups.filter(name='Dealer').exists():
            return qs.filter(dealer_id=request.user.pk)
        return qs

    def save_model(self, request, obj, form, change):
        """Changes method save.


        If the user is authenticated and belongs to the group equals to
        'Dealer', when creates another user, it is added dealer_is equals
        id user is authenticated.
        """
        if request.user.groups.filter(name='Dealer').exists():
            obj.dealer_id = request.user.pk
        super().save_model(request, obj, form, change)


class GroupAdminWithCount(GroupAdmin):
    """Class is representation of a model Group in the admin interface."""

    list_display = GroupAdmin.list_display + ('user_count',)

    def user_count(self, obj):
        """Counts the number of users in a group."""

        return obj.user_set.count()


admin.site.unregister(Group)
admin.site.register(Group, GroupAdminWithCount)
admin.site.register(models.User, UserAdmin)
