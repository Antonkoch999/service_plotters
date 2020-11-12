"""Classes and methods of models `Lable` and `Template for admin page."""
from random import randint

from django.contrib import admin
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path

from import_export import resources
from import_export.admin import ImportExportMixin

from main_service_of_plotters.apps.users.models import User
from main_service_of_plotters.apps.materials.models import Label, Template
from .forms import (SelectUserForm, SelectDealerForm, LabelFormDealer,
                    LabelFormUser, LabelFormAdmin, GenerationCodeForm)


@staff_member_required
def generation_code(request):
    if request.method == "POST":
        form = GenerationCodeForm(request.POST)
        if form.is_valid():
            count_label = form.cleaned_data['count_label']
            count = form.cleaned_data['count']
            # size = form.cleaned_data['size']
            for _ in range(count_label):
                scratch_code = randint(1000000000000000, 9999999999999999)
                while Label.objects.filter(scratch_code=scratch_code).exists():
                    scratch_code = randint(1000000000000000, 9999999999999999)
                barcode = randint(1000000000000000, 9999999999999999)
                while Label.objects.filter(barcode=barcode).exists():
                    barcode = randint(1000000000000000, 9999999999999999)

                Label.objects.create(
                    scratch_code=scratch_code,
                    barcode=barcode,
                    count=count,
                    # size=size,
                )
            return HttpResponseRedirect('../')

    else:
        form = GenerationCodeForm()
    return render(request, 'admin/generation_code.html', {'form': form})


class LabelResource(resources.ModelResource):
    """Model Resourse for django-import-export."""

    class Meta:
        model = Label


class CustomLabelAdmin(ImportExportMixin, admin.ModelAdmin):
    """`Label` admin page."""

    # import resource class for working django-import-export
    resource_class = LabelResource
    search_fields = ('barcode',)
    # custom actions
    actions = ['add_user', 'add_dealer']

    @staticmethod
    def add_user(request, queryset):
        """Add user as owner for set of labels."""

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
            form = SelectUserForm(
                initial={
                    '_selected_action':
                        request.POST.getlist(admin.ACTION_CHECKBOX_NAME)},
                dealer=request.user)
            queryset = queryset.filter(user=None)
            return render(request, 'admin/multiple_owner_change.html',
                          {'items': queryset, 'form': form,
                           'title': u'Изменение категории'})

    @staticmethod
    def add_dealer(request, queryset):
        """Add dealer as owner for set in labels."""

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
        elif request.user.groups.filter(name='User').exists():
            del actions['add_dealer']
            del actions['add_user']
        return actions

    def get_queryset(self, request):
        """Change list of available labels depended of logged user."""

        qs = super().get_queryset(request)
        # Dealer can see own labels
        if request.user.groups.filter(name='Dealer').exists():
            qs = qs.filter(dealer=request.user.pk)
        # User can see only own labels
        elif request.user.groups.filter(name='User').exists():
            qs = qs.filter(user=request.user.pk)
        return qs

    def get_form(self, request, obj=None, **kwargs):
        """Change form of admin page depended of logged user."""

        if request.user.groups.filter(name='Dealer').exists():
            kwargs['form'] = LabelFormDealer
            # Dealer can add to label only user it own
            form = super().get_form(request, obj, **kwargs)
            form.base_fields['user'].queryset = User.objects.filter(
                dealer=request.user)
            # For dealer barcode is unchangable
            form.base_fields['barcode'].disabled = True
            if obj.user is not None:
                form.base_fields['user'].disabled = True
        elif request.user.groups.filter(name='User').exists():
            kwargs['form'] = LabelFormUser
        elif request.user.groups.filter(name='Administrator').exists():
            kwargs['form'] = LabelFormAdmin
            form = super().get_form(request, obj, **kwargs)
            if obj is not None and obj.dealer is not None:
                form.base_fields['dealer'].disabled = True
        return super().get_form(request, obj, **kwargs)

    def get_list_display(self, request):
        """Change list_display list depended of logged user."""

        list_display = ('scratch_code', 'barcode',
                        'count', 'available_count', 'dealer', 'user',
                        'date_of_expiration',
                        'is_active',)
        # If user is `Dealer` or User
        if self._is_requested_user_dealer_or_user(request):
            # without `scretch code`
            list_display = ['barcode', 'count', 'available_count',
                            'dealer', 'user', 'date_of_expiration',
                            'days_before_expiration', 'is_active',
                            ]
        return list_display

    def get_list_filter(self, request):
        """Add filters on list page depeded of logged user."""

        filters = ('date_creation', 'user', 'dealer',)
        if CustomLabelAdmin._is_requested_user_dealer_or_user(request):
            filters = ('date_creation',)
        return filters

    @staticmethod
    def _is_requested_user_dealer_or_user(request):
        """Identificate is authenticated user is dealer."""
        return request.user.groups.filter(name='Dealer').exists() or request.user.groups.filter(name='User').exists()

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [path("generation_code/", generation_code,
                        name='generation code'), ]
        return my_urls + urls


class TemplateAdmin(admin.ModelAdmin):
    """Class for `Template` admin representation."""

    list_display = ('name', 'device_category', 'manufacturer_category',
                    'file_photo', 'file_plt', 'size')
    exclude = ('date_creation',)


admin.site.register(Template, TemplateAdmin)
admin.site.register(Label, CustomLabelAdmin)
