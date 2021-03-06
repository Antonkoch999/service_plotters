"""This module create forms."""

from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from main_service_of_plotters.apps.users.models import User


class UserCreationForm(forms.ModelForm):
    """Creates form for creation user, using model User."""

    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Password confirmation'),
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'username', 'role', 'dealer')

    def clean_password2(self):
        """Validate password."""

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        """Hashes the password."""

        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class DealerUserForm(UserCreationForm):
    """Creates form for creating users by dealer, using model User."""

    role = forms.ChoiceField(choices=[
        ('User', _('User'))
    ], label=_('User role'))


class AdministratorUserForm(UserCreationForm):
    """Creates form for creating dealer by Administrator, using model User."""

    role = forms.ChoiceField(choices=[
        ('Dealer', _('Dealer'))
    ], label=_('User role'))


class UserChangeForm(forms.ModelForm):
    """Creates form for change user, using model User."""

    class Meta:
        model = User
        fields = ('email', 'username', 'role', 'dealer', 'password')
