from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Ticket, PopularProblem
from main_service_of_plotters.apps.device.models import Plotter

WARIANT_NOT_PRESENTED = 'wariant_not_presented'


def _list_of_popular_problems_plus_not_found():
    choices = [
        (f"{pp.id}", pp.name)
        for pp
        in PopularProblem.objects.all()
    ]
    choices.append((WARIANT_NOT_PRESENTED, _("My problem is not presented in this list")))
    return choices


class ChoosePopularProblemForm(forms.Form):
    plotters = forms.ModelMultipleChoiceField(queryset=Plotter.objects)
    problem = forms.ChoiceField(
        choices=_list_of_popular_problems_plus_not_found
    )

    def __init__(self, *args, context=None, **kwargs):
        super().__init__(*args, **kwargs)
        if context is not None:
            request = context.get('request')
            self.fields['plotters'].queryset = request.user.plotter_user


class DetailedProblemFrom(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = (
            'header',
            'text',
            'media_file',
            'plotters'
        )

    def __init__(self, *args, context = None, **kwargs):
        super().__init__(*args, **kwargs)
        # plotters field is read only
        self.fields['plotters'].disabled = True
        # limit only user's potters
        if context is not None:
            request = context.get('request')
            self.fields['plotters'].queryset = request.user.plotter_user


class TechSpecialistForm(forms.ModelForm):

    class Meta:
        models = Ticket
        fields = ['header', 'text', 'media_file', 'status', 'assignee',
                  'answer']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['header'].disabled = True
        self.fields['text'].disabled = True
        self.fields['media_file'].disabled = True

