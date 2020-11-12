import pytest
from django.test import RequestFactory

from ..models import Plotter
from ..api.views import PlotterViewSet
from .test_admin import create_group, create_user

pytestmark = pytest.mark.django_db


class TestPlotterViewSet:

    def __init__(self):
        group = create_group()
        user = create_user()

        self.admin = user['Administrator']
        self.dealer = user['Dealer']
        self.user = user['User']

        # Assign Groups
        self.admin.groups.add(group['Administrator'])
        self.dealer.groups.add(group['Dealer'])
        self.user.groups.add(group['User'])

        self.view = PlotterViewSet()

        self.plotter1 = Plotter.objects.create(
            serial_number=1,
        )
        self.plotter2 = Plotter.objects.create(
            serial_number=2,
            dealer=self.dealer
        )
        self.plotter2 = Plotter.objects.create(
            serial_number=3,
            dealer=self.dealer,
            user=self.user
        )

    def test_get_queryset_admin_see_all(self):
        request = RequestFactory().get(path='/fake-url/')
        request.user = self.admin
        self.view.request = request

        assert self.view.filter_queryset(self.view.get_queryset()).count() == Plotter.objects.all().count()

    def test_get_queryset_dealer_see_only_owned(self):
        request = RequestFactory().get(path='/fake-url/')
        dealer = self.dealer
        request.user = dealer
        self.view.request = request
        qs = self.view.filter_queryset(self.view.get_queryset())

        assert qs.count() > 0
        assert qs.count() == Plotter.objects.filter(dealer=dealer).count()

        for plotter in qs:
            assert plotter.dealer == dealer

    def test_get_queryset_user_see_only_owned(self):
        request = RequestFactory().get(path='/fake-url/')
        user = self.user
        request.user = user
        self.view.request = request
        qs = self.view.filter_queryset(self.view.get_queryset())

        assert qs.count() > 0
        assert qs.count() == Plotter.objects.filter(user=user).count()

        for plotter in qs:
            assert plotter.user == user
