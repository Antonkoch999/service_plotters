from django.views import View
from django.views.generic import ListView
from .models import StatisticsPlotter


class StatisticsPlotterView(ListView):
    queryset = StatisticsPlotter.objects.all()


