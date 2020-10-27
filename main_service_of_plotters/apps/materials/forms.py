"""This module creates form."""

from django import forms
from main_service_of_plotters.apps.materials.models import Label
from main_service_of_plotters.apps.users.models import User


class SelectDealerForm(forms.Form):
    """From with one field `dealer` to add this dealer to multiple entities."""

    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    dealer = forms.ModelChoiceField(
        queryset=User.objects.filter(role='Dealer'),
        label=u'Dealer')


class SelectUserForm(forms.Form):
    """From with one field `user` to add this user to multiple entities."""

    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(role='User'),
        label=u'User')

    def __init__(self, *args, dealer=None, **kwargs):
        super().__init__(*args, **kwargs)
        # while form is created, filter by owner user
        if dealer:
            self.fields['user'].queryset = \
                User.objects.filter(dealer_id=dealer.pk)


class LabelFormDealer(forms.ModelForm):
    """Form for `Label` admin page when `User` is loggined."""

    class Meta:
        models = Label
        # User must't see scrathc_code at own dealer (its obviouse)
        exclude = ('dealer', 'scratch_code')


class LabelFormUser(forms.ModelForm):
    """Form for `Label` admin page when `Dealer` is loggined."""

    class Meta:
        models = Label
        exclude = ('user', 'dealer', 'scratch_code')
