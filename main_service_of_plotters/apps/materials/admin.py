from django.contrib import admin
from django import forms
from import_export import resources
from import_export.admin import ImportExportMixin
from django.shortcuts import render
from .forms import SelectUserForm, SelectDealerForm
from django.http import HttpResponseRedirect
from main_service_of_plotters.apps.users.models import User

from main_service_of_plotters.apps.materials.models import Label, Template


class LabelResource(resources.ModelResource):
    class Meta:
        model = Label


class LabelFormDealer(forms.ModelForm):
    class Meta:
        models = Label
        exclude = ('dealer', 'scratch_code')


class LabelFormUser(forms.ModelForm):
    class Meta:
        models = Label
        exclude = ('user', 'dealer', 'scratch_code')


class CustomLabelAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = LabelResource
    list_display = ('scratch_code', 'barcode', 'date_creation', 'date_update',
                    'count', 'dealer', 'user')
    list_filter = ('date_creation',)
    search_fields = ('date_creation',)
    actions = ['add_user', 'add_dealer']

    def add_user(self, request, queryset):
        form = None

        if 'apply' in request.POST:
            form = SelectUserForm(request.POST)

            if form.is_valid():
                user = form.cleaned_data['user']

                for item in queryset:
                    item.user = user
                    item.save()

                return HttpResponseRedirect(request.get_full_path())

        if not form:
            form = SelectUserForm(initial={
                '_selected_action': request.POST.getlist(
                    admin.ACTION_CHECKBOX_NAME)})
            return render(request, 'admin/multiple_owner_change.html',
                          {'items': queryset, 'form': form,
                           'title': u'Изменение категории'})

    def add_dealer(self, request, queryset):
        form = None

        if 'apply' in request.POST:
            form = SelectDealerForm(request.POST)

            if form.is_valid():
                dealer = form.cleaned_data['dealer']

                for item in queryset:
                    item.dealer = dealer
                    item.save()

                return HttpResponseRedirect(request.get_full_path())

        if not form:
            form = SelectDealerForm(initial={
                '_selected_action': request.POST.getlist(
                    admin.ACTION_CHECKBOX_NAME)})
            return render(request, 'admin/add_dealer.html',
                          {'items': queryset, 'form': form,
                           'title': u'Изменение категории'})

    def get_actions(self, request):
        actions = super().get_actions(request)
        if request.user.groups.filter(name='Dealer').exists():
            del actions['add_dealer']
        elif request.user.groups.filter(name='Administrator').exists():
            del actions['add_user']
        return actions

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.filter(name='Dealer').exists():
            return qs.filter(dealer=request.user.pk)
        elif request.user.groups.filter(name='User').exists():
            return qs.filter(user=request.user.pk)
        return qs

    def get_form(self, request, obj=None, **kwargs):
        if request.user.role == 'Dealer':
            kwargs['form'] = LabelFormDealer
            form = super().get_form(request, obj, **kwargs)
            form.base_fields['user'].queryset = User.objects.filter(
                dealer_id=request.user.pk)
            form.base_fields['barcode'].disabled = True
            return form
        elif request.user.role == 'User':
            kwargs['form'] = LabelFormUser
        return super().get_form(request, obj, **kwargs)

    def get_list_display(self, request):
        if request.user.groups.filter(name='Dealer').exists() \
                or request.user.groups.filter(name='User').exists():
            return ['barcode', 'date_creation', 'date_update',
                    'count', 'dealer', 'user']
        return super().get_list_display(request)


class TemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'device_category', 'manufacturer_category',
                    'file_photo', 'file_plt', 'date_creation', 'date_update')


admin.site.register(Template, TemplateAdmin)
admin.site.register(Label, CustomLabelAdmin)
