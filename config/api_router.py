from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework.urls import path

from main_service_of_plotters.apps.category.api.views import (
    DeviceCategoryViewSet, ManufacturerViewSet, ModelsTemplateViewSet)
from main_service_of_plotters.apps.device.api.views import PlotterViewSet, cut
from main_service_of_plotters.apps.materials.api.views import (LabelViewSet,
                                                               TemplateViewSet)
from main_service_of_plotters.apps.statistics.api.views import (
    CuttingTransactionViewSet, StatisticsPlotterViewSet,
    StatisticsTemplateViewSet)
from main_service_of_plotters.apps.users.api.views import UserViewSet


if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("plotters", PlotterViewSet)
router.register("templates", TemplateViewSet)
router.register("labels", LabelViewSet)
router.register("devicecategory", DeviceCategoryViewSet)
router.register("manufacturer", ManufacturerViewSet)
router.register("modelstemplate", ModelsTemplateViewSet)
router.register("statisticsplotter", StatisticsPlotterViewSet)
router.register("statisticstemplate", StatisticsTemplateViewSet)
router.register("cuttingtransaction", CuttingTransactionViewSet)


app_name = "api"

additional_urls = [
    path('cut/', cut, name='cut'),
]

urlpatterns = router.urls + additional_urls
