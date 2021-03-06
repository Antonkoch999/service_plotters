from django import forms
from django.utils.translation import gettext_lazy as _

from main_service_of_plotters.apps.device.models import Plotter
from .models import Ticket, PopularProblem

VARIANT_NOT_PRESENTED = 'variant_not_presented'


def _list_of_popular_problems_plus_not_found():
    choices = [
        (str(pp.id), pp.name)
        for pp
        in PopularProblem.objects.all()
    ]
    choices.append((VARIANT_NOT_PRESENTED, _("My problem is not presented in this list")))
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

    def __init__(self, *args, context=None, **kwargs):
        super().__init__(*args, **kwargs)
        # limit only user's potters
        if context is not None:
            request = context.get('request')
            self.fields['plotters'].queryset = request.user.plotter_user


class TechSpecialistForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ['header', 'text', 'media_file', 'status', 'plotters',
                  'assignee', 'answer', 'answer_attached_file']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['header'].disabled = True
        self.fields['text'].disabled = True
        self.fields['media_file'].disabled = True
        self.fields['plotters'].disabled = True


class UserForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ['header', 'text', 'media_file', 'status', 'plotters',
                  'assignee', 'answer', 'answer_attached_file']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].disabled = True
        self.fields['plotters'].disabled = True
        self.fields['assignee'].disabled = True
        self.fields['answer'].disabled = True
        self.fields['answer_attached_file'].disabled = True
