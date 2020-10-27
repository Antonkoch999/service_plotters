"""Classes and methods of models `Lable` and `Template for admin page."""

from django.contrib import admin
from django.shortcuts import render
from django.http import HttpResponseRedirect
from import_export import resources
from import_export.admin import ImportExportMixin


from main_service_of_plotters.apps.users.models import User
from main_service_of_plotters.apps.materials.models import Label, Template
from .forms import SelectUserForm, SelectDealerForm, LabelFormDealer, LabelFormUser


class LabelResource(resources.ModelResource):
    """Model Resourse for django-import-export."""

    class Meta:
        model = Label


class CustomLabelAdmin(ImportExportMixin, admin.ModelAdmin):
    """`Label` admin page."""

    # import resource class for working django-import-export
    resource_class = LabelResource
    list_display = ('scratch_code', 'barcode', 'date_creation', 'date_update',
                    'count', 'dealer', 'user', 'is_active')
    list_filter = ('date_creation', 'user', 'dealer')
    search_fields = ('barcode',)
    # custom actions
    actions = ['add_user', 'add_dealer']

    def add_user(self, request, queryset):
        """Action to add user as owner for set of labels."""

        form = None

        if 'apply' in request.POST:
            form = SelectUserForm(request.POST)

            if form.is_valid():
                user = form.cleaned_data['user']

                for item in queryset:
                    if item.user is None:
                        item.user = user
                        item.save()

                return HttpResponseRedirect(request.get_full_path())

        if not form:
            form = SelectUserForm(initial={
                '_selected_action': request.POST.getlist(
                    admin.ACTION_CHECKBOX_NAME)},
                dealer=request.user)
            queryset = queryset.filter(user=None)
            return render(request, 'admin/multiple_owner_change.html',
                          {'items': queryset, 'form': form,
                           'title': u'Изменение категории'})

    def add_dealer(self, request, queryset):
        """Action to add dealer as owner for set in labels."""

        form = None

        if 'apply' in request.POST:
            form = SelectDealerForm(request.POST)

            if form.is_valid():
                dealer = form.cleaned_data['dealer']

                for item in queryset:
                    if item.dealer is None:
                        item.dealer = dealer
                        item.save()

                return HttpResponseRedirect(request.get_full_path())

        if not form:
            form = SelectDealerForm(initial={
                '_selected_action': request.POST.getlist(
                    admin.ACTION_CHECKBOX_NAME)})
            queryset = queryset.filter(dealer=None)
            return render(request, 'admin/add_dealer.html',
                          {'items': queryset, 'form': form,
                           'title': u'Изменение категории'})

    def get_actions(self, request):
        """Change list of actions for different users."""

        actions = super().get_actions(request)
        if request.user.groups.filter(name='Dealer').exists():
            del actions['add_dealer']
        elif request.user.groups.filter(name='Administrator').exists():
            del actions['add_user']
        return actions

    def get_queryset(self, request):
        """Change list of available labels depended of logged user."""

        qs = super().get_queryset(request)
        # Dealer can see own labels
        if request.user.groups.filter(name='Dealer').exists():
            return qs.filter(dealer=request.user.pk)
        # User can see only own labels
        elif request.user.groups.filter(name='User').exists():
            return qs.filter(user=request.user.pk)
        return qs

    def get_form(self, request, obj=None, **kwargs):
        """Change form of admin page depended of logged user."""

        if request.user.role == 'Dealer':
            kwargs['form'] = LabelFormDealer
            # Dealer can add to label only user it own
            form = super().get_form(request, obj, **kwargs)
            form.base_fields['user'].queryset = User.objects.filter(
                dealer_id=request.user.pk)
            # For dealer barcode is unchangable
            form.base_fields['barcode'].disabled = True
            if obj.user is not None:
                form.base_fields['user'].disabled = True
            return form
        elif request.user.role == 'User':
            kwargs['form'] = LabelFormUser
        elif request.user.role == 'Administrator':
            form = super().get_form(request, obj, **kwargs)
            if obj.dealer is not None:
                form.base_fields['dealer'].disabled = True
            return form
        return super().get_form(request, obj, **kwargs)

    def get_list_display(self, request):
        """Change list_display list depended of logged user."""

        # If user is `Dealer` or User
        if CustomLabelAdmin._is_requested_user_dealer_or_user(request):
            # without `scretch code`
            return ['barcode', 'date_creation', 'date_update',
                    'count', 'dealer', 'user', 'is_active']
        return super().get_list_display(request)

    @staticmethod
    def _is_requested_user_dealer_or_user(request):
        """Helper method identificate is authenticated user is dealer."""

        return request.user.groups.filter(name='Dealer').exists() \
            or request.user.groups.filter(name='User').exists()


class TemplateAdmin(admin.ModelAdmin):
    """Class for `Template` admin representation."""

    list_display = ('name', 'device_category', 'manufacturer_category',
                    'file_photo', 'file_plt', 'date_creation', 'date_update')


admin.site.register(Template, TemplateAdmin)
admin.site.register(Label, CustomLabelAdmin)
