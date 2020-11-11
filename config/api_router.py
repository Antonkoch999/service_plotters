from django.conf import settings
from rest_framework.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from main_service_of_plotters.apps.device.api.views import PlotterViewSet, cut, PlotterViewSetByDID, scratch_code

from main_service_of_plotters.apps.users.api.views import UserViewSet

from main_service_of_plotters.apps.materials.api.views import TemplateViewSet, LabelViewSet
from main_service_of_plotters.apps.category.api.views import (
    DeviceCategoryViewSet, ManufacturerViewSet, ModelsTemplateViewSet)
from main_service_of_plotters.apps.statistics.api.views import (
    StatisticsPlotterViewSet, StatisticsTemplateViewSet,
    CuttingTransactionViewSet)

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
    path('plotter-by-did/<str:device_id>/', PlotterViewSetByDID.as_view({'get': 'retrieve'}), name='plotter-by-did'),
    path('addlabel/', scratch_code, name='scratch_code'),
]

urlpatterns = router.urls + additional_urls
