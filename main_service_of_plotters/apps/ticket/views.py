from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic.edit import CreateView

from .models import Ticket, PopularProblem
from .forms import ChoosePopularProblemForm, WARIANT_NOT_PRESENTED
from main_service_of_plotters.apps.device.models import Plotter

STEP_1_ACTION = 'step_1'


# Create your views here.
class UserAddTicket(View):
    def get(self, request):
        form = ChoosePopularProblemForm(context={'request': request})
        context = {'form': form}
        context['action'] = STEP_1_ACTION
        return render(
            request,
            template_name='ticket/add_ticket.html',
            context=context
        )

    def post(self, request):
        print(request.POST)
        action = request.POST.get('action')
        if action is not None \
                and action[0] == STEP_1_ACTION\
                and problem[0] == WARIANT_NOT_PRESENTED:
            # Do things when user chose not presented problemn
            pass
        else:
            # Choosed popular problem, populate it
            form = ChoosePopularProblemForm(request.POST)
            if form.is_valid():
                chosed_problem = get_object_or_404(
                    PopularProblem,
                    pk=form.cleaned_data['problem']
                )
                ticket = Ticket.objects.create(
                    header=chosed_problem.populated_header,
                    text=chosed_problem.populated_text,
                    reporter=request.user
                )
                ticket.plotters.set(form.cleaned_data["plotters"])

                return redirect('tickets:user_add_ticket')
            else:
                return redirect('tickets:user_add_ticket')
