from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter
from django.urls import include, path
from django.conf.urls import url
from main_service_of_plotters.apps.users.api.views import (
    api_root, UserListView, UserRegisterView, UserDetailView)

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()


app_name = "api"
urlpatterns = [
    path('', api_root),
    path('users', UserListView.as_view(), name='user'),
    path('registrations/', UserRegisterView.as_view(), name='registrations'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail')
]

