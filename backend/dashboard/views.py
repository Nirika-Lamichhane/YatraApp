# dashboard/views.py

# ------------------- DRF imports -------------------
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

# -------------------Accounts app imports -------------------
from accounts.models import Destination, DestinationType

# ------------------- Models and serializers -------------------
from .models import Place, Hotel, Food, Activity, Favorite, Comment
from .serializers import (
    PlaceSerializer, HotelSerializer, FoodSerializer, ActivitySerializer,
    FavoriteSerializer, CommentSerializer
)

# ------------------- ML helpers -------------------
from .ml.dataLoader import load_all_data
from .ml.clustering import cluster_for_dashboard


# ------------------- CRUD APIs -------------------

class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer


class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer


class FoodViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically attach the logged-in user to the favorite
        serializer.save(user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically attach the logged-in user to the comment
        serializer.save(user=self.request.user)


# ------------------- Recommendation API -------------------

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommend_view(request):
    """
    Returns personalized recommendations for the logged-in user.
    Uses favorites and comments for collaborative filtering.
    """

    user_id = request.user.id  # Get the logged-in user ID

    # get query parameters
    destination_id= request.GET.get('destination_id', None)
    item_type=request.GET.get('item_type', 'places')  # 'place', 'hotel', 'food', 'activity' and default is places

    # Load necessary data from DB
    destination_types= DestinationType.objects.all()
    destinations= Destination.objects.all()

    # Step 1: Load all necessary tables into pandas DataFrames
    places, activities, foods, hotels, user_interactions = load_all_data()

    # filter by destination if provided
    if destination_id:
        destination_id=int(destination_id)
        if item_type=='places':
            df=places.filter(destination_id=destination_id)
        elif item_type=='hotels':
            df=hotels.filter(destination_id=destination_id)
        elif item_type=='foods':
            df=foods.filter(destination_id=destination_id)
        elif item_type=='activities':
            df=activities.filter(destination_id=destination_id)
        else:
            return Response({"error": "Invalid item_type"}, status=400)
    
        
    