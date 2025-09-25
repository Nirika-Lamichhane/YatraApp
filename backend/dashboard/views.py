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
   
   user_id=request.user.id
   # load all data from db to dataframes
   destinations, destination_types,places_df, activities_df, foods_df, hotels_df, user_interactions = load_all_data()

   # we have to choose which to cluster in the dashboard
   item_type = request.GET.get("item_type", "places")  # default = places
   destination_id = request.GET.get("destination_id", None)

   if not destination_id:
       return Response({"error":" Please select a destination first."}, staus=404)

   destination_id = int(destination_id)

   # filter items by destination
   if item_type == "places":
       
       df_filtered = places_df[places_df["destination_id"] == destination_id]
       numeric_features = ["rating"]
       category_prefix="place"

   elif item_type == "hotels":
        df_filtered = hotels_df[hotels_df["place_id"].isin(
            places_df[places_df["destination_id"] == destination_id]["id"]
        )]
        numeric_features = ["rating", "price_range"]
        category_prefix="hotel"

   elif item_type == "foods":
        df_filtered = foods_df[foods_df["place_id"].isin(
            places_df[places_df["destination_id"] == destination_id]["id"]
        )]
        numeric_features = ["rating", "price_range"]
        category_prefix="food"

   elif item_type == "activities":
        df_filtered = activities_df[activities_df["place_id"].isin(
            places_df[places_df["destination_id"] == destination_id]["id"]
        )]
        numeric_features = ["rating", "price_range"]
        category_prefix="activity"

   else:
        return Response({"error": "Invalid item_type"}, status=400)
   
   
      
   # preparing user interactions for collaborative filtering

   user_favorites = user_interactions.get("favorites", [])
   user_ratings = user_interactions.get("ratings", [])
   user_comments = user_interactions.get("comments", [])
   destination_links = user_interactions.get("destination_links", {})
   place_links = user_interactions.get("place_links", {})
   


    # now applying clustering
   badge_mapping={
        0:"Budget",
        1:"Mid range",
        2:"Luxury"
    }
   df_clustered=cluster_for_dashboard(df_filtered,numeric_features, n_clusters=3, badge_mapping=badge_mapping)

   # convert clustered df to django orm for the serialization and returing responses
   ids = df_clustered["id"].tolist()
   if item_type == "places":
        queryset = Place.objects.filter(id__in=ids)
        serializer = PlaceSerializer(queryset, many=True)
   elif item_type == "hotels":
        queryset = Hotel.objects.filter(id__in=ids)
        serializer = HotelSerializer(queryset, many=True)
   elif item_type == "foods":
        queryset = Food.objects.filter(id__in=ids)
        serializer = FoodSerializer(queryset, many=True)
   elif item_type == "activities":
        queryset = Activity.objects.filter(id__in=ids)
        serializer = ActivitySerializer(queryset, many=True)
   
   # return the response to the fluter frontend
   return Response({
        "user_id": user_id,
        "destination_id": destination_id,
        "item_type": item_type,
        "clustered_data": serializer.data
    }, status=200)







   """  
   here the data is loaded from database into the dataframes as python objects
   and clustering is applied to them 
   then this data is fetched using orm using clustered ids
   serialize and returned  as json responses to use by flutter
   """

    