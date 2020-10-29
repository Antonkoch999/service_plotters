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
            dealer_id=self.user_dealer.pk,
        )

        self.user = User.objects.create_user(
            username='test_user',
            email='test_user@test_user.com',
            password='test1user',
            dealer_id=self.user_dealer.pk,
        )

        self.user_administrator.groups.add(self.group_administrator)
        self.user_dealer.groups.add(self.group_dealer)
        self.user_user.groups.add(self.group_user)

        self.user_administrator.save()
        self.user_dealer.save()
        self.user_user.save()

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
