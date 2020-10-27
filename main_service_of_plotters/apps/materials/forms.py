from django import forms
from main_service_of_plotters.apps.materials.models import Label
from main_service_of_plotters.apps.users.models import User


class SelectDealerForm(forms.Form):
    '''From with one field `dealer` to add this dealer to multiple entities.'''
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    dealer = forms.ModelChoiceField(
        queryset=User.objects.filter(role='Dealer'),
        label=u'Dealer')


class SelectUserForm(forms.Form):
    '''From with one field `user` to add this user to multiple entities.'''
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(role='User'),
        label=u'User')


class LabelFormDealer(forms.ModelForm):
    '''Form for `Label` admin page when `User` is loggined.'''

    class Meta:
        models = Label
        # User must't see scrathc_code at own dealer (its obviouse)
        exclude = ('dealer', 'scratch_code')


class LabelFormUser(forms.ModelForm):
    '''Form for `Label` admin page when `Dealer` is loggined.'''

    class Meta:
        models = Label
        exclude = ('user', 'dealer', 'scratch_code')
