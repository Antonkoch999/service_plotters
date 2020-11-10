""" Unit tests for ticket app forms."""
import pytest
from django.test import RequestFactory
from django.contrib.auth import get_user_model

from ..forms import ChoosePopularProblemForm, DetailedProblemFrom, \
                    VARIANT_NOT_PRESENTED, TechSpecialistForm, UserForm
from ..models import PopularProblem
from main_service_of_plotters.apps.device.models import Plotter
from main_service_of_plotters.apps.users.constants import ROLE

pytestmark = pytest.mark.django_db
User = get_user_model()


class TestTicketFormsChoosePopularForm:
    def setup(self):
        self.dealer = User.objects.create(
            username='dealer',
            password='dealer',
            role=ROLE['Dealer']
        )
        self.user1 = User.objects.create(
            username='user1',
            password='user1',
            dealer=self.dealer
        )
        self.user2 = User.objects.create(
            username='user2',
            password='user2',
            dealer=self.dealer
        )

        self.plotter1 = Plotter.objects.create(
            dealer=self.dealer,
            user=self.user1,
            serial_number=1111222233334444,
        )
        self.plotter2 = Plotter.objects.create(
            dealer=self.dealer,
            user=self.user1,
            serial_number=1111222233334445,
        )
        self.plotter3 = Plotter.objects.create(
            dealer=self.dealer,
            user=self.user2,
            serial_number=1111222233334446,
        )
        self.popular_problem1 = PopularProblem.objects.create(
            name='name',
            populated_header='pop1'
        )
        self.popular_problem2 = PopularProblem.objects.create(
            name='name',
            populated_header='pop2'
        )

    def test_user_can_see_only_own_plotters_in_list(self):
        request = RequestFactory().get('fake')
        request.user = self.user1
        form = ChoosePopularProblemForm(context={'request': request})
        plotters_list = list(form.fields['plotters'].queryset.all())
        assert len(plotters_list) == self.user1.plotter_user.count()
        for plotter in self.user1.plotter_user.all():
            assert plotter in plotters_list
        assert self.plotter3 not in plotters_list

    def test_all_problems_presented_plus_variant_not_presented(self):
        form = ChoosePopularProblemForm()
        choices = list(form.fields['problem'].choices)
        assert len(choices) == 3
        assert VARIANT_NOT_PRESENTED in dict(choices).keys()
        assert str(self.popular_problem1.pk) in dict(choices).keys()
        assert str(self.popular_problem2.pk) in dict(choices).keys()


class TestTicketFormsDetailedForm:
    def setup(self):
        self.dealer = User.objects.create(
            username='dealer',
            password='dealer',
            role=ROLE['Dealer']
        )
        self.user1 = User.objects.create(
            username='user1',
            password='user1',
            dealer=self.dealer
        )
        self.user2 = User.objects.create(
            username='user2',
            password='user2',
            dealer=self.dealer
        )
        self.plotter1 = Plotter.objects.create(
            dealer=self.dealer,
            user=self.user1,
            serial_number=1111222233334444,
        )
        self.plotter2 = Plotter.objects.create(
            dealer=self.dealer,
            user=self.user1,
            serial_number=1111222233334445,
        )
        self.plotter3 = Plotter.objects.create(
            dealer=self.dealer,
            user=self.user2,
            serial_number=1111222233334446,
        )

    def test_header_field_in_detailed_form(self):
        form = DetailedProblemFrom()
        assert 'header' in form.fields

    def test_text_field_in_detailed_form(self):
        form = DetailedProblemFrom()
        assert 'text' in form.fields

    def test_media_file_field_in_detailed_form(self):
        form = DetailedProblemFrom()
        assert 'media_file' in form.fields

    def test_reporter_field_not_presented(self):
        """Cause must be populated automaticaly depended of authorized user."""
        form = DetailedProblemFrom()
        assert 'reporter' not in form.fields

    def test_user_can_see_only_own_plotters_in_list(self):
        request = RequestFactory().get('fake')
        request.user = self.user1
        form = ChoosePopularProblemForm(context={'request': request})
        plotters_list = list(form.fields['plotters'].queryset.all())
        assert len(plotters_list) == self.user1.plotter_user.count()
        for plotter in self.user1.plotter_user.all():
            assert plotter in plotters_list
        assert self.plotter3 not in plotters_list


class ModelFieldsCheckMixin:

    def setup(self, form_class):
        self.form = form_class()

    def assert_field_presented_and_disabled(self, field):
        self.assert_field_presented(field)
        self.assert_field_disabled(field)

    def assert_field_presented(self, field):
        assert field in self.form.fields.keys(), "field is not presented"

    def assert_field_not_presented(self, field):
        assert field not in self.form.fields.keys(), 'field is presented'

    def assert_field_disabled(self, field):
        assert self.form.fields[field].disabled, "field is not disabled"


class TestTechSpecialistForm(ModelFieldsCheckMixin):
    def setup(self):
        super().setup(TechSpecialistForm)

    def test_techspec_header_field_presented_and_disabled(self):
        self.assert_field_presented_and_disabled('header')

    def test_techspec_text_field_presented_and_disabled(self):
        self.assert_field_presented_and_disabled('text')

    def test_techspec_media_file_field_presented_and_disabled(self):
        self.assert_field_presented_and_disabled('media_file')

    def test_techspec_plotters_field_presented_and_disabled(self):
        self.assert_field_presented_and_disabled('plotters')

    def test_answer_field_presented(self):
        self.assert_field_presented('answer')

    def test_answer_attached_file_field_presented(self):
        self.assert_field_presented('answer_attached_file')

    def test_reporter_field_not_presented(self):
        self.assert_field_not_presented('reporter')


class TestUserForm(ModelFieldsCheckMixin):
    def setup(self):
        super().setup(UserForm)

    def test_assignee_header_field_presented_and_disabled(self):
        self.assert_field_presented_and_disabled('assignee')

    def test_techspec_answer_field_presented_and_disabled(self):
        self.assert_field_presented_and_disabled('answer')

    def test_techspec_answer_attached_file_field_presented_and_disabled(self):
        self.assert_field_presented_and_disabled('answer_attached_file')
