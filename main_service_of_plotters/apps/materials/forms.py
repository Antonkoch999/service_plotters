"""This module creates form."""

from django import forms
from django.utils.translation import gettext_lazy as _

from main_service_of_plotters.apps.materials.models import Label
from main_service_of_plotters.apps.users.models import User


class GenerationCodeForm(forms.ModelForm):
    """From with one field `dealer` to add this dealer to multiple entities."""
    count_label = forms.IntegerField(label=_('Count label'))

    class Meta:
        model = Label
        fields = ['count', 'count_label', ]


class SelectDealerForm(forms.Form):
    """From with one field `dealer` to add this dealer to multiple entities."""

    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    dealer = forms.ModelChoiceField(
        queryset=User.objects.filter(role='Dealer'),
        label=_('Dealer'))


class SelectUserForm(forms.Form):
    """From with one field `user` to add this user to multiple entities."""

    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(role='User'),
        label=_('User'))

    def __init__(self, *args, dealer=None, **kwargs):
        super().__init__(*args, **kwargs)
        # while form is created, filter by owner user
        if dealer:
            self.fields['user'].queryset = \
                User.objects.filter(dealer=dealer)


class LabelFormDealer(forms.ModelForm):
    """Form for `Label` admin page when `User` is loggined."""

    class Meta:
        models = Label
        # User must't see scratch_code at own dealer (its obviouse)
        fields = ('barcode', 'count', 'user', )


class LabelFormUser(forms.ModelForm):
    """Form for `Label` admin page when `Dealer` is loggined."""

    class Meta:
        models = Label
        fields = ('barcode', 'count', 'date_of_activation', 'linked_plotter', )


class LabelFormAdmin(forms.ModelForm):
    """Form for `Label` admin page when `Administrator` is loggined."""

    class Meta:
        models = Label
        fields = ('scratch_code', 'barcode', 'count', 'dealer', 'user',
                  'is_active', )
