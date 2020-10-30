import pytest
from django.test import RequestFactory
from django.contrib.auth.models import Group

from ..models import Plotter
from ..api.views import PlotterViewSet
from ...users.models import User
from ...users.constants import ROLE

pytestmark = pytest.mark.django_db


class TestPlotterViewSet:
    def setup(self):
        self.admin = User.objects.create(
            username='admin',
            password='admin',
            role=ROLE['Administrator']
        )
        self.dealer = User.objects.create(
            username='dealer',
            password='dealer',
            role=ROLE['Dealer']
        )
        self.user = User.objects.create(
            username='user',
            password='user',
            dealer_id=self.dealer
        )
        # Create groups
        self.group_administrator = Group.objects.get_or_create(
            name='Administrator')[0]
        self.group_dealer = Group.objects.get_or_create(name='Dealer')[0]
        self.group_user = Group.objects.get_or_create(name='User')[0]

        # Assign Groups
        self.admin.groups.add(self.group_administrator)
        self.dealer.groups.add(self.group_dealer)
        self.user.groups.add(self.group_user)

        self.view = PlotterViewSet()

        self.plotter1 = Plotter.objects.create(
            serial_number=1,
            available_film=1
        )
        self.plotter2 = Plotter.objects.create(
            serial_number=2,
            available_film=2,
            dealer=self.dealer
        )
        self.plotter2 = Plotter.objects.create(
            serial_number=3,
            available_film=3,
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



