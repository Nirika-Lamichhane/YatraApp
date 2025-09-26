from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlaceViewSet, HotelViewSet, FoodViewSet, ActivityViewSet, FavoriteViewSet, CommentViewSet, recommend_view  , SubmitRatingView   

router = DefaultRouter()
router.register(r'places', PlaceViewSet)
router.register(r'hotels', HotelViewSet)
router.register(r'foods', FoodViewSet)
router.register(r'activities', ActivityViewSet)
router.register(r'favorites', FavoriteViewSet)
router.register(r'comments', CommentViewSet)


urlpatterns = [
    path('', include(router.urls)), # this is for viewsets
    path('recommend/', recommend_view, name='recommend'), # this is for recommendation API
    path ('rate/', SubmitRatingView.as_view(), name='submit_rating'), # this is for rating items

]
