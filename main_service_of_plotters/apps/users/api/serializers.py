from rest_framework import serializers
from main_service_of_plotters.apps.users.models import User


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'password', 'url']
        extra_kwargs = {
            'url': {
                'view_name': 'api:user-detail'
            },
        }


class UserListSerializerForAdministrator(UserListSerializer):

    role = serializers.ChoiceField(choices=[
        ('Dealer', 'Dealer')
    ])


class UserListSerializerForDealer(UserListSerializer):

    role = serializers.ChoiceField(choices=[
        ('User', 'User')
    ])


