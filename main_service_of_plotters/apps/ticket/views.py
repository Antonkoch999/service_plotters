from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseNotFound
from django.contrib.auth import get_user_model

from .models import Ticket, PopularProblem
from .forms import ChoosePopularProblemForm, WARIANT_NOT_PRESENTED, DetailedProblemFrom
from main_service_of_plotters.apps.device.models import Plotter



# TODO add permissions -- authenticated user and permissions
class UserAddTicket(LoginRequiredMixin, PermissionRequiredMixin, View):

    permission_required = ('ticket.add_ticket',)

    _STEP_1_ACTION = 'step_1'
    _STEP_2_ACTION = 'step_2'

    def get(self, request):
        form = ChoosePopularProblemForm(context={'request': request})
        context = {
            'form': form,
            'action': self._STEP_1_ACTION
        }
        return render(
            request,
            template_name='ticket/add_ticket.html',
            context=context
        )

    def post(self, request):
        self.request = request
        if self._is_popular_problem_choosed:
            return self._process_choosed_popular_problem(request)
        elif self._is_warriant_not_presented_choosed:
            return self._process_warriant_not_presented(request)
        elif self._is_detailed_problem_passed:
            return self._process_detailed_problem_passed(request)
        else:
            return HttpResponseNotFound()

    @property
    def _is_popular_problem_choosed(self):
        return self._returned_after_page_with_popular_problem \
            and self.request.POST.get('problem') != WARIANT_NOT_PRESENTED

    @property
    def _is_warriant_not_presented_choosed(self):
        return self._returned_after_page_with_popular_problem \
            and self.request.POST.get('problem') == WARIANT_NOT_PRESENTED

    @property
    def _is_detailed_problem_passed(self):
        return self._returned_after_page_with_detailed_problem

    @property
    def _returned_after_page_with_popular_problem(self):
        return self.request.POST.get('action') == self._STEP_1_ACTION

    @property
    def _returned_after_page_with_detailed_problem(self):
        return self.request.POST.get('action') == self._STEP_2_ACTION

    def _process_choosed_popular_problem(self, request):
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

            return self._problem_posted_redirect()

    def _process_warriant_not_presented(self, request):
        prev_form = ChoosePopularProblemForm(request.POST)
        prev_form.is_valid()
        choosed_plotters = prev_form.cleaned_data['plotters']
        form = DetailedProblemFrom(
            context={'request': request},
            initial={'plotters': choosed_plotters})
        context = {
            'action': self._STEP_2_ACTION,
            'form': form}
        return render(request, 'ticket/add_ticket.html', context)

    def _process_detailed_problem_passed(self, request):
        form = DetailedProblemFrom(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.reporter = request.user
            ticket.save()
            ticket.plotters.set(form.cleaned_data['plotters'])
            ticket.save()
            print(ticket)
            return self._problem_posted_redirect()
        else:
            print(form.errors)
            return HttpResponseNotFound()

    def _problem_posted_redirect(self):
        return redirect('tickets:user_add_ticket')
