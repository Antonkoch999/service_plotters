from rest_framework import serializers
from main_service_of_plotters.apps.users.models import User


class UserListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'dealer_id', 'role', 'url']
        extra_kwargs = {
            'url': {
                'view_name': 'api:user-detail'
            }
        }

