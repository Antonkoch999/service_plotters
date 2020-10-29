from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from main_service_of_plotters.apps.users.api.views import UserViewSet
from main_service_of_plotters.apps.device.api.views import PlotterViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("plotters", PlotterViewSet)


app_name = "api"
urlpatterns = router.urls
