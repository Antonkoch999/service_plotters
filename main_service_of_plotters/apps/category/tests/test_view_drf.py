import json

from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from main_service_of_plotters.apps.users.models import User
from main_service_of_plotters.apps.category.models import (DeviceCategory,
                                                           ModelsTemplate,
                                                           Manufacturer)
from main_service_of_plotters.apps.device.tests.test_admin import (create_user,
                                                                   create_group)


class UsersTestCase(APITestCase):

    def setUp(self):
        group = create_group()
        user = create_user()
        self.admin = user['Administrator']
        self.dealer = user['Dealer']
        self.user = user['User']

        self.admin.groups.add(group['Administrator'])
        self.dealer.groups.add(group['Dealer'])
        self.user.groups.add(group['User'])

        self.admin.save()
        self.dealer.save()
        self.user.save()

        self.devicecategory = DeviceCategory.objects.create(
            name='Devicecategory',
        )
        self.manufacturer = Manufacturer.objects.create(
            device_category=self.devicecategory,
            name='Manufacturer',
        )
        self.modelstemplate = ModelsTemplate.objects.create(
            manufacturer=self.manufacturer,
            name='modelstemplate',
        )

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

    def test_get_devicecategory_detail_administrator(self):
        self.client.login(username='administrator', password='administrator')
        response = self.client.get(
            reverse('api:devicecategory-detail',
                    kwargs={'pk': self.devicecategory.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_devicecategory_detail_dealer(self):
        self.client.login(username='dealer', password='dealer')
        response = self.client.get(
            reverse('api:devicecategory-detail',
                    kwargs={'pk': self.devicecategory.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_devicecategory_detail_user(self):
        self.client.login(username='user', password='user')
        response = self.client.get(
            reverse('api:devicecategory-detail',
                    kwargs={'pk': self.devicecategory.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_manufacturer_detail_administrator(self):
        self.client.login(username='administrator', password='administrator')
        response = self.client.get(
            reverse('api:manufacturer-detail',
                    kwargs={'pk': self.manufacturer.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_manufacturer_detail_dealer(self):
        self.client.login(username='dealer', password='dealer')
        response = self.client.get(
            reverse('api:manufacturer-detail',
                    kwargs={'pk': self.manufacturer.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_manufacturer_detail_user(self):
        self.client.login(username='user', password='user')
        response = self.client.get(
            reverse('api:manufacturer-detail',
                    kwargs={'pk': self.manufacturer.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_modelstemplate_detail_administrator(self):
        self.client.login(username='administrator', password='administrator')
        response = self.client.get(
            reverse('api:modelstemplate-detail',
                    kwargs={'pk': self.modelstemplate.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_modelstemplate_detail_dealer(self):
        self.client.login(username='dealer', password='dealer')
        response = self.client.get(
            reverse('api:modelstemplate-detail',
                    kwargs={'pk': self.modelstemplate.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_modelstemplate_detail_user(self):
        self.client.login(username='user', password='user')
        response = self.client.get(
            reverse('api:modelstemplate-detail',
                    kwargs={'pk': self.modelstemplate.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_devicecategory_data_administrator(self):
        self.client.login(username='administrator', password='administrator')
        response = self.client.get(reverse('api:devicecategory-list'))
        data = [
            {'id': self.devicecategory.pk,
             'name': self.devicecategory.name,
             'photo': None,
             'url': f'http://testserver/api/devicecategory/{self.devicecategory.pk}/'
             }
        ]
        self.assertEqual(json.loads(response.content), data)

    def test_get_devicecategory_data_detail_administrator(self):
        self.client.login(username='administrator', password='administrator')
        response = self.client.get(
            reverse('api:devicecategory-detail',
                    kwargs={'pk': self.devicecategory.pk}))
        data = {
            'id': self.devicecategory.pk,
            'name': self.devicecategory.name,
            'photo': None,
            'url': f'http://testserver/api/devicecategory/{self.devicecategory.pk}/',
            'device': [f'http://testserver/api/manufacturer/{self.manufacturer.pk}/']
        }

        self.assertEqual(json.loads(response.content), data)

    def test_get_manufacturer_data_administrator(self):
        self.client.login(username='administrator', password='administrator')
        response = self.client.get(reverse('api:manufacturer-list'))
        data = [
            {'id': self.manufacturer.pk,
             'device_category': f'http://testserver/api/devicecategory/{self.manufacturer.pk}/',
             'name': self.manufacturer.name,
             'photo': None,
             'url': f'http://testserver/api/manufacturer/{self.manufacturer.pk}/'
             }
        ]
        self.assertEqual(json.loads(response.content), data)

    def test_get_manufacturer_data_detail_administrator(self):
        self.client.login(username='administrator', password='administrator')
        response = self.client.get(
            reverse('api:manufacturer-detail',
                    kwargs={'pk': self.manufacturer.pk}))
        data = {
            'id': self.manufacturer.pk,
            'device_category': f'http://testserver/api/devicecategory/{self.manufacturer.pk}/',
            'name': self.manufacturer.name,
            'photo': None,
            'url': f'http://testserver/api/manufacturer/{self.manufacturer.pk}/',
            'modelstemplate': [f'http://testserver/api/modelstemplate/{self.modelstemplate.pk}/']
        }
        self.assertEqual(json.loads(response.content), data)

    def test_get_modelstemplate_data_administrator(self):
        self.client.login(username='administrator', password='administrator')
        response = self.client.get(reverse('api:modelstemplate-list'))
        data = [{
            'id': self.modelstemplate.pk,
            'manufacturer': f'http://testserver/api/manufacturer/{self.modelstemplate.pk}/',
            'name': self.modelstemplate.name,
            'url': f'http://testserver/api/modelstemplate/{self.modelstemplate.pk}/',
            'template_set': []}]
        self.assertEqual(json.loads(response.content), data)
