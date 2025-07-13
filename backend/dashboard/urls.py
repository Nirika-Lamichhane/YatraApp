from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlaceViewSet, HotelViewSet, FoodViewSet, ActivityViewSet

router = DefaultRouter()
router.register(r'places', PlaceViewSet)
router.register(r'hotels', HotelViewSet)
router.register(r'foods', FoodViewSet)
router.register(r'activities', ActivityViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
