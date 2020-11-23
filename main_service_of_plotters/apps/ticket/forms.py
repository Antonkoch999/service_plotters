"""This module creates form."""

from django import forms
from django.utils.translation import gettext_lazy as _

from main_service_of_plotters.apps.device.models import Plotter
from .models import Ticket, PopularProblem

VARIANT_NOT_PRESENTED = 'variant_not_presented'


def _list_of_popular_problems_plus_not_found():
    """Create list, what display category popular problem."""
    choices = [
        (str(pp.id), pp.name)
        for pp
        in PopularProblem.objects.all()
    ]
    choices.append((VARIANT_NOT_PRESENTED,
                    _("My problem is not presented in this list")))
    return choices


class ChoosePopularProblemForm(forms.Form):
    """This class create form with list popular problem and users plotter."""

    plotters = forms.ModelMultipleChoiceField(queryset=Plotter.objects)
    problem = forms.ChoiceField(
        choices=_list_of_popular_problems_plus_not_found
    )

    def __init__(self, *args, context=None, **kwargs):
        """Filter plotter dependent on user."""
        super().__init__(*args, **kwargs)
        if context is not None:
            request = context.get('request')
            self.fields['plotters'].queryset = request.user.plotter_user


class DetailedProblemFrom(forms.ModelForm):
    """This class create form for new ticket if problem isn't popular."""

    class Meta:
        """Metadata of Ticket."""

        model = Ticket
        fields = (
            'header',
            'text',
            'media_file',
            'plotters'
        )

    def __init__(self, *args, context=None, **kwargs):
        """Filter plotter dependent on user."""
        super().__init__(*args, **kwargs)
        # limit only user's potters
        if context is not None:
            request = context.get('request')
            self.fields['plotters'].queryset = request.user.plotter_user


class TechSpecialistForm(forms.ModelForm):
    """This class create form for TechSpecialist for model Ticket."""

    status = forms.ChoiceField(choices=[
        ('W', _('In Work')),
        ('S', _('Solved')),
    ], label=_('Status'))

    class Meta:
        """Metadata of Ticket."""

        model = Ticket
        fields = ['header', 'text', 'media_file', 'status', 'plotters',
                  'assignee', 'answer', 'answer_attached_file']

    def __init__(self, *args, **kwargs):
        """Make fields disabled."""
        super().__init__(*args, **kwargs)
        self.fields['header'].disabled = True
        self.fields['text'].disabled = True
        self.fields['media_file'].disabled = True
        self.fields['plotters'].disabled = True


class UserForm(forms.ModelForm):
    """This class create form for User for model Ticket."""

    def __init__(self, *args, **kwargs):
        """Make fields disabled."""
        super().__init__(*args, **kwargs)
        self.fields['status'].disabled = True
        self.fields['plotters'].disabled = True
        self.fields['assignee'].disabled = True
        self.fields['answer'].disabled = True
        self.fields['answer_attached_file'].disabled = True

    class Meta:
        """Metadata of Ticket."""

        model = Ticket
        fields = ['header', 'text', 'media_file', 'status', 'plotters',
                  'assignee', 'answer', 'answer_attached_file']
