from main_service_of_plotters.apps.users.models import User
from rest_framework.viewsets import ModelViewSet
from .serializers import (
    UserListSerializer, UserListSerializerForAdministrator,
    UserListSerializerForDealer)
from .permissions import UserPermission
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password


@permission_classes([IsAuthenticated, UserPermission])
class UserViewSet(ModelViewSet):
    serializer_class = UserListSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        qs = User.objects.all()
        if self.request.user.groups.filter(name='Dealer').exists():
            qs = User.objects.filter(dealer_id=self.request.user.pk)
        elif self.request.user.groups.filter(name='Administrator').exists():
            qs = User.objects.all()
        return qs

    def get_serializer_class(self):
        serializer_class = UserListSerializer
        if self.request.user.groups.filter(name='Dealer').exists():
            serializer_class = UserListSerializerForDealer
        elif self.request.user.groups.filter(name='Administrator').exists():
            serializer_class = UserListSerializerForAdministrator

        return serializer_class

    def perform_create(self, serializer):
        if self.request.user.groups.filter(name='Dealer').exists():
            serializer.save(
                dealer_id=self.request.user.pk,
                password=make_password(self.request.data['password']))
        else:
            serializer.save(
                password=make_password(self.request.data['password']))
