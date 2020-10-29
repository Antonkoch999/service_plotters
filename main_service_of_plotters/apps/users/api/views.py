
from django.contrib.auth import get_user_model
from rest_framework import status, request
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from .serializers import UserListSerializer, UserRegisterSerializer, UserDetailList
from main_service_of_plotters.apps.users.models import User


@api_view(['GET'])
def api_root(request) -> Response:
    """Entry endpoints of our API.
    :param request: HTTP GET request
    :return:        Instance of Response class
    """
    return Response({
        'user': reverse('api:user', request=request),
        'registrations': reverse('api:registrations', request=request),
    })


class UserListView(generics.ListAPIView):
    serializer_class = UserListSerializer
    queryset = User.objects.all()


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserDetailList
    queryset = User.objects.all()
