from django import forms

from main_service_of_plotters.apps.users.models import User

USERS = [(user, user.get_full_name()) for user in User.objects.filter(role='Dealer')]


class TaskAdminForm(forms.ModelForm):
    class Meta:
        model = User
    user = forms.ChoiceField(choices=USERS)
