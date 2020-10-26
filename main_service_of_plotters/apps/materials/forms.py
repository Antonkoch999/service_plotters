from django import forms
from main_service_of_plotters.apps.materials.models import Label
from main_service_of_plotters.apps.users.models import User


class SelectDealerForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    dealer = forms.ModelChoiceField(
        queryset=User.objects.filter(role='Dealer'),
        label=u'Dealer')


class SelectUserForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(role='User'),
        label=u'User')
