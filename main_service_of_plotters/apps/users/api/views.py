from main_service_of_plotters.apps.users.models import User
from rest_framework.viewsets import ModelViewSet
from .serializers import UserListSerializer


class UserViewSet(ModelViewSet):
    serializer_class = UserListSerializer
    queryset = User.objects.all()
