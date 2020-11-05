from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Ticket, PopularProblem


def _list_of_popular_problems_plus_not_found():
        choices = [
            (f"popular_problem.{pp.id}", pp.name)
            for pp
            in PopularProblem.objects.all()
        ]
        choices.append(('wariant_not_presented', _("My problem is not presented in this list")))
        return choices


class ChoosePopularProblemForm(forms.Form):
    plotters = forms.ModelMultipleChoiceField(queryset=None)
    problem = forms.ChoiceField(
        choices=_list_of_popular_problems_plus_not_found
    )

    def __init__(self, *args, context, **kwargs):
        super().__init__(*args, **kwargs)
        request = context.get('request')
        self.fields['plotters'].queryset = request.user.plotter_user


