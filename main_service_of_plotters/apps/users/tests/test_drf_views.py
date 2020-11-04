from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from main_service_of_plotters.apps.users.models import User
from django.contrib.auth.models import Group
from main_service_of_plotters.apps.users.api.views import UserViewSet


class UsersTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user_administrator = User.objects.create_user(
            username='administrator',
            email='administrator@administrator.com',
            password='administrator',
            role='Administrator'
        )
        self.user_dealer = User.objects.create_user(
            username='dealer',
            email='dealer@dealer.com',
            password='dealer',
            role='Dealer'
        )
        self.user_user = User.objects.create_user(
            username='user',
            email='user',
            password='user',
            dealer=self.user_dealer,
            role='User'
        )

        self.user = User.objects.create_user(
            username='test_user',
            email='test_user@test_user.com',
            password='test1user',
            dealer=self.user_dealer,
        )

        self.view = UserViewSet()

    def test_get_user_list_administrator(self):
        self.client.login(username='administrator', password='administrator')
        response = self.client.get(reverse('api:user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_list_dealer(self):
        self.client.login(username='dealer', password='dealer')
        response = self.client.get(reverse('api:user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_list_user(self):
        self.client.login(username='user', password='user')
        response = self.client.get(reverse('api:user-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_user_list_administrator(self):
        self.client.login(username='administrator', password='administrator')
        data = {
            'username': 'test', 'email': 'test@test.com',
            'role': 'Dealer', 'password': 'test',
            }
        response = self.client.post(reverse('api:user-list'),
                                    data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_user_list_dealer(self):
        self.client.login(username='dealer', password='dealer')
        data = {
            'username': 'test', 'email': 'test@test.com',
            'role': 'User', 'password': 'test',
            }
        response = self.client.post(reverse('api:user-list'),
                                    data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_user_list_user(self):
        self.client.login(username='user', password='user')
        data = {
            'username': 'test', 'email': 'test@test.com',
            'role': 'User', 'password': 'test',
            }
        response = self.client.post(reverse('api:user-list'),
                                    data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_user_detail_administrator(self):
        self.client.login(username='administrator', password='administrator')
        data = {
            'username': 'test', 'email': 'test@test.com',
            'role': 'Dealer', 'password': 'test',
        }
        response = self.client.put(reverse('api:user-detail',
                                           kwargs={"pk": self.user.pk}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.user.id)
        self.assertEqual(response.data['username'], 'test')
        self.assertEqual(response.data['email'], 'test@test.com')
        self.assertEqual(response.data['password'], 'test')

    def test_put_user_detail_dealer(self):
        self.client.login(username='dealer', password='dealer')
        data = {
            'username': 'test', 'email': 'test@test.com',
            'role': 'User', 'password': 'test',
        }
        response = self.client.put(reverse('api:user-detail',
                                           kwargs={"pk": self.user.pk}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.user.id)
        self.assertEqual(response.data['username'], 'test')
        self.assertEqual(response.data['email'], 'test@test.com')
        self.assertEqual(response.data['password'], 'test')

    def test_put_user_detail_user(self):
        self.client.login(username='user', password='user')
        data = {
            'username': 'test', 'email': 'test@test.com',
            'role': 'User', 'password': 'test',
        }
        response = self.client.put(reverse('api:user-detail',
                                           kwargs={"pk": self.user.pk}), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_user_detail_administrator(self):
        self.client.login(username='administrator', password='administrator')
        response = self.client.delete(reverse(
            'api:user-detail',
            kwargs={"pk": self.user.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_user_detail_dealer(self):
        self.client.login(username='dealer', password='dealer')
        response = self.client.delete(reverse(
            'api:user-detail',
            kwargs={"pk": self.user.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_user_detail_user(self):
        self.client.login(username='user', password='user')
        response = self.client.delete(reverse(
            'api:user-detail',
            kwargs={"pk": self.user.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
