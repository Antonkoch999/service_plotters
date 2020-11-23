"""Set of models serializer."""

from rest_framework import serializers
from main_service_of_plotters.apps.users.models import User


class UserListSerializer(serializers.ModelSerializer):
    """Typical user model serializer."""

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'password', 'url']
        extra_kwargs = {
            'url': {
                'view_name': 'api:user-detail'
            },
        }


class UserListSerializerForAdministrator(UserListSerializer):
    """User model serializer how it administrator see."""

    role = serializers.ChoiceField(choices=[
        ('Dealer', 'Dealer')
    ])


class UserListSerializerForDealer(UserListSerializer):
    """User model serializer how it dealer see."""

    role = serializers.ChoiceField(choices=[
        ('User', 'User')
    ])
