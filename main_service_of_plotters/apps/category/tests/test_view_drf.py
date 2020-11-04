from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from main_service_of_plotters.apps.users.models import User
from django.contrib.auth.models import Group
from main_service_of_plotters.apps.users.api.views import UserViewSet


class UsersTestCase(APITestCase):

    def setUp(self):
        self.group_administrator = Group.objects.get_or_create(
            name='Administrator')[0]
        self.group_dealer = Group.objects.get_or_create(name='Dealer')[0]
        self.group_user = Group.objects.get_or_create(name='User')[0]
        self.client = APIClient()
        self.user_administrator = User.objects.create_user(
            username='administrator',
            email='administrator@administrator.com',
            password='administrator',
        )
        self.user_dealer = User.objects.create_user(
            username='dealer',
            email='dealer@dealer.com',
            password='dealer',
        )
        self.user_user = User.objects.create_user(
            username='user',
            email='user',
            password='user',
            dealer=self.user_dealer,
        )

        self.user_administrator.groups.add(self.group_administrator)
        self.user_dealer.groups.add(self.group_dealer)
        self.user_user.groups.add(self.group_user)

        self.user_administrator.save()
        self.user_dealer.save()
        self.user_user.save()

    def test_get_devicecategory_list_administrator(self):
        self.client.login(username='administrator', password='administrator')
        response = self.client.get(reverse('api:devicecategory-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_devicecategory_list_dealer(self):
        self.client.login(username='dealer', password='dealer')
        response = self.client.get(reverse('api:devicecategory-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_devicecategory_list_user(self):
        self.client.login(username='user', password='user')
        response = self.client.get(reverse('api:devicecategory-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_manufacturer_list_administrator(self):
        self.client.login(username='administrator', password='administrator')
        response = self.client.get(reverse('api:manufacturer-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_manufacturer_list_dealer(self):
        self.client.login(username='dealer', password='dealer')
        response = self.client.get(reverse('api:manufacturer-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_manufacturer_list_user(self):
        self.client.login(username='user', password='user')
        response = self.client.get(reverse('api:manufacturer-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_modelstemplate_list_administrator(self):
        self.client.login(username='administrator', password='administrator')
        response = self.client.get(reverse('api:modelstemplate-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_modelstemplate_list_dealer(self):
        self.client.login(username='dealer', password='dealer')
        response = self.client.get(reverse('api:modelstemplate-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_modelstemplate_list_user(self):
        self.client.login(username='user', password='user')
        response = self.client.get(reverse('api:modelstemplate-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
