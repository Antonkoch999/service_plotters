from django import forms
from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError

from main_service_of_plotters.apps.users.models import User


class UserCreationForm(forms.ModelForm):

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'username', 'role', 'dealer_id')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class DealerUserForm(UserCreationForm):
    role = forms.ChoiceField(choices=[
        ('User', 'User')
    ])


class AdministratorUserForm(UserCreationForm):
    role = forms.ChoiceField(choices=[
        ('Dealer', 'Dealer')
    ])


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'role', 'dealer_id')

    def clean_password(self):
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    def get_form(self, request, obj=None, **kwargs):
        if request.user.role == 'Dealer':
            kwargs['form'] = DealerUserForm
        elif request.user.role == 'Administrator':
            kwargs['form'] = AdministratorUserForm
        return super().get_form(request, obj, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.filter(name='Dealer').exists():
            return qs.filter(dealer_id=request.user.pk)
        return qs

    list_display = ('username', 'email', 'role', 'dealer_id')
    list_filter = ('role',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'first_name', 'last_name',
                           'role', 'password', 'is_active',
                           )}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'role', 'password1',
                       'password2'),
        }),
    )
    search_fields = ('role',)

    def save_model(self, request, obj, form, change):
        if request.user.groups.filter(name='Dealer').exists():
            obj.dealer_id = request.user.pk
        super().save_model(request, obj, form, change)


class GroupAdminWithCount(GroupAdmin):

    def user_count(self, obj):
        return obj.user_set.count()

    list_display = GroupAdmin.list_display + ('user_count',)


admin.site.unregister(Group)
admin.site.register(Group, GroupAdminWithCount)
admin.site.register(User, UserAdmin)
