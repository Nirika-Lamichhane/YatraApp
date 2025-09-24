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
   
   
   # load all data from db to dataframes
   destinations, destination_types,places_df, activities_df, foods_df, hotels_df, user_interactions = load_all_data()

   # we have to choose which to cluster in the dashboard
   item_type = request.GET.get("item_type", "places")  # default = places
   destination_id = request.GET.get("destination_id", None)

   if not destination_id:
       return Response({"error":" Please select a destination first."}, staus=404)

   destination_id = int(destination_id)

   






   """  
   here the data is loaded from database into the dataframes as python objects
   and clustering is applied to them 
   then this data is fetched using orm using clustered ids
   serialize and returned  as json responses to use by flutter
   """

    