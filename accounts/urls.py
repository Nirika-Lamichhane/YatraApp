from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('destination-types/', views.get_destination_types, name='destination_types'),
    path('destinations/', views.get_destinations_by_types, name='destinations_by_type'),
    path('favorites/', views.submit_favorite_destinations, name='submit_favorites'),
    path('favorites/user/', views.get_user_favorites, name='get_user_favorites'),
]
