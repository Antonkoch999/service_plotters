'''Classes and methods of models `Lable` and `Template for admin page.'''

from django.contrib import admin
from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from import_export import resources
from import_export.admin import ImportExportMixin


from main_service_of_plotters.apps.users.models import User
from main_service_of_plotters.apps.materials.models import Label, Template
from .forms import SelectUserForm, SelectDealerForm, LabelFormDealer, LabelFormUser


class LabelResource(resources.ModelResource):
    '''Model Resourse for django-import-export.'''

    class Meta:
        model = Label


class CustomLabelAdmin(ImportExportMixin, admin.ModelAdmin):
    '''`Label` admin page.'''

    # import resource class for working django-import-export
    resource_class = LabelResource
    list_display = ('scratch_code', 'barcode', 'date_creation', 'date_update',
                    'count', 'dealer', 'user')
    list_filter = ('date_creation',)
    search_fields = ('barcode',)
    # custom actions
    actions = ['add_user', 'add_dealer']

    def _add_generic_user(self, request, queryset,
                          instance_field_name: str,
                          user_form: forms.Form,
                          template_path: str):
        '''Generic method ads action views for two actions below.'''

        form = None
        # Actions when pressed 'submit'
        if 'apply' in request.POST:
            # Get form for request
            form = user_form(request.POST)

            if form.is_valid():
                # get choosen instance to add in set of labels
                instance_field = form.cleaned_data[instance_field_name]

                # update all of labels in instance (owner) field
                for item in queryset:
                    item_changing_field = item.get_field(instance_field_name)
                    item_changing_field = instance_field
                    item.save()

                return HttpResponseRedirect(request.get_full_path())
        # Actions when action is choosed
        if not form:
            # render view with form and template
            form = user_form(initial={
                '_selected_action': request.POST.getlist(
                    admin.ACTION_CHECKBOX_NAME)})
            return render(request, template_path,
                          {'items': queryset, 'form': form,
                           'title': f'Change {instance_field_name} for multiple labels'})

    def add_user(self, request, queryset):
        '''Action to add user as owner for set of labels.'''

        return self._add_generic_user(request, queryset, 'user', SelectUserForm, 'admin/multiple_owner_change.html')

    def add_dealer(self, request, queryset):
        '''Action toi add dealer as owner for set in labels.'''

        return self._add_generic_user(request, queryset, 'dealer', SelectDealerForm, 'admin/add_dealer.html')

    def get_actions(self, request):
        '''Change list of actions for different users'''

        actions = super().get_actions(request)
        if request.user.groups.filter(name='Dealer').exists():
            del actions['add_dealer']
        elif request.user.groups.filter(name='Administrator').exists():
            del actions['add_user']
        return actions

    def get_queryset(self, request):
        '''Change list of available labels depended of logged user.'''

        qs = super().get_queryset(request)
        # Dealer can see own labels
        if request.user.groups.filter(name='Dealer').exists():
            return qs.filter(dealer=request.user.pk)
        # User can see only own labels
        elif request.user.groups.filter(name='User').exists():
            return qs.filter(user=request.user.pk)
        return qs

    def get_form(self, request, obj=None, **kwargs):
        '''Change form of admin page depended of logged user.'''

        if request.user.role == 'Dealer':
            kwargs['form'] = LabelFormDealer
            # Dealer can add to label only user it own
            form = super().get_form(request, obj, **kwargs)
            form.base_fields['user'].queryset = User.objects.filter(
                dealer_id=request.user.pk)
            # For dealer barcode is unchangable
            form.base_fields['barcode'].disabled = True
            return form
        elif request.user.role == 'User':
            kwargs['form'] = LabelFormUser
        return super().get_form(request, obj, **kwargs)

    def get_list_display(self, request):
        '''Change list_display list depended of logged user.'''

        # If user is `Dealer` or User
        if CustomLabelAdmin._is_requested_user_dealer_or_user(request):
            # without `scretch code`
            return ['barcode', 'date_creation', 'date_update',
                    'count', 'dealer', 'user']
        return super().get_list_display(request)

    @staticmethod
    def _is_requested_user_dealer_or_user(request):
        '''Helper method identificate is authenticated user is dealer.'''

        return request.user.groups.filter(name='Dealer').exists() \
            or request.user.groups.filter(name='User').exists()


class TemplateAdmin(admin.ModelAdmin):
    '''Class for `Template` admin representation.'''
    list_display = ('name', 'device_category', 'manufacturer_category',
                    'file_photo', 'file_plt', 'date_creation', 'date_update')


admin.site.register(Template, TemplateAdmin)
admin.site.register(Label, CustomLabelAdmin)
