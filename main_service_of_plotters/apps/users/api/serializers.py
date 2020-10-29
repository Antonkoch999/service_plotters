from rest_framework import serializers
from main_service_of_plotters.apps.users.models import User


class UserListSerializer(serializers.HyperlinkedModelSerializer):
    user_detail = serializers.HyperlinkedIdentityField(
        view_name='api:user-detail')

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'dealer_id', 'role',
                  'user_detail')


class UserDetailList(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email',
                  'dealer_id', 'role',)


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

