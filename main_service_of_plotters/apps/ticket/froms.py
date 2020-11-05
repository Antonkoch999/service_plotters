from django import forms

from .models import Ticket, PopularProblem

class ChoosePopularProblemFrom(forms.Form):
    problem = forms.ChoiceField(
        choices=list_of_popular_problems
    )
