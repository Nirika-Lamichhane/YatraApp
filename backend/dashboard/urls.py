from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlaceViewSet, HotelViewSet, FoodViewSet, ActivityViewSet, FavoriteViewSet, CommentViewSet        

router = DefaultRouter()
router.register(r'places', PlaceViewSet)
router.register(r'hotels', HotelViewSet)
router.register(r'foods', FoodViewSet)
router.register(r'activities', ActivityViewSet)
router.register(r'favorites', FavoriteViewSet)
router.register(r'comments', CommentViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
