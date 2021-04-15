from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from api.views import CrashViewSet, PlaceViewSet, HarmedViewSet, VehicleViewSet, StationViewSet

router=DefaultRouter()
router.register('crash',CrashViewSet, basename='crash')
router.register('harmed',HarmedViewSet, basename='harmed')
router.register('vehicle',VehicleViewSet, basename='vehicle')
router.register('station',StationViewSet, basename='station')

urlpatterns = [
    path('', include(router.urls)),
    re_path('place/', PlaceViewSet.as_view()),
]