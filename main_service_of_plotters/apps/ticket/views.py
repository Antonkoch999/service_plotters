from django.shortcuts import render
from django.views import View
from django.views.generic.edit import CreateView

from .models import Ticket
from .froms import ChoosePopularProblemForm


# Create your views here.
class UserAddTicket(View):
    def get(self, request):
        form = ChoosePopularProblemForm(context={'request': request})
        context = {'form': form}
        return render(
            request,
            template_name='ticket/add_ticket.html',
            context=context
        )
