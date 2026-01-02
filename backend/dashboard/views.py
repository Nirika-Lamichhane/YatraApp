# dashboard/views.py

# ------------------- DRF imports -------------------
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

# -------------------- rating model -------------------
from .models import Rating
from django.contrib.contenttypes.models import ContentType
from django.db.models import Avg
from rest_framework.views import APIView
from rest_framework import status,permissions

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
from .ml.collaborative import build_interactions, create_user_item_matrix, calculate_user_similarity, get_recommendations


# ------------------- CRUD APIs -------------------

class PlaceViewSet(viewsets.ModelViewSet):
    serializer_class = PlaceSerializer
    
    def get_queryset(self):
        """Filter Places by the Destination ID provided in the URL"""
        queryset = Place.objects.all()
        dest_id = self.request.query_params.get('dest_id')
        if dest_id:
            queryset = queryset.filter(destination_id=dest_id)
        return queryset


class HotelViewSet(viewsets.ModelViewSet):
    serializer_class = HotelSerializer
    
    def get_queryset(self):
        """Filter Hotels by Destination (via the Place relationship)"""
        queryset = Hotel.objects.all()
        dest_id = self.request.query_params.get('dest_id')
        if dest_id:
            # We filter through the 'place' foreign key to get to 'destination'
            queryset = queryset.filter(place__destination_id=dest_id)
        return queryset


class FoodViewSet(viewsets.ModelViewSet):
    serializer_class = FoodSerializer
    
    def get_queryset(self):
        """Filter Food by Destination (via the Place relationship)"""
        queryset = Food.objects.all()
        dest_id = self.request.query_params.get('dest_id')
        if dest_id:
            queryset = queryset.filter(place__destination_id=dest_id)
        return queryset


class ActivityViewSet(viewsets.ModelViewSet):
    serializer_class = ActivitySerializer
    
    def get_queryset(self):
        """Filter Activities by Destination (via the Place relationship)"""
        queryset = Activity.objects.all()
        dest_id = self.request.query_params.get('dest_id')
        if dest_id:
            queryset = queryset.filter(place__destination_id=dest_id)
        return queryset

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

# ------------------- Rating API -------------------#

class SubmitRatingView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Generic endpoint for submitting rating for any model:
        POST body: {
            "model": "place",  # "hotel", "food", "activity"
            "object_id": 3,
            "rating": 4.5
        }
        """
        user = request.user
        model_name = request.data.get('model')
        object_id = request.data.get('object_id')
        rating_value = request.data.get('rating')

        if not model_name or not object_id or not rating_value:
            return Response({"error": "model, object_id, and rating are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Get content type dynamically
        try:
            content_type = ContentType.objects.get(model=model_name)
        except ContentType.DoesNotExist:
            return Response({"error": "Invalid model name"}, status=status.HTTP_400_BAD_REQUEST)

        # Update or create the rating
        rating_obj, created = Rating.objects.update_or_create(
            user=user,
            content_type=content_type,
            object_id=object_id,
            defaults={'rating': rating_value}
        )

        return Response({"message": "Rating submitted successfully"}, status=status.HTTP_200_OK)

# ------------------- Recommendation API -------------------

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommend_view(request):
   
   user_id=request.user.id
   # load all data from db to dataframes
   destinations, destination_types,places_df, activities_df, foods_df, hotels_df, user_interactions = load_all_data()
   destination_id = request.GET.get("dest_id") or request.GET.get("destination_id")
   item_type = request.GET.get("item_type", "places")


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

   # build interactions dataframe

   interactions_df = build_interactions(
       user_favorites, user_ratings, user_comments,
       destination_links, place_links)
   user_item_matrix= create_user_item_matrix(interactions_df)
   user_similarity= calculate_user_similarity(user_item_matrix)

   # collaborative filtering recommendations

   if user_id in user_item_matrix.index and user_item_matrix.loc[user_id].sum()>0:
       # user has previous interactions so cf
       cf_recommendations_ids= get_recommendations(
           user_id, user_item_matrix, user_similarity,
           top_n=10, category=category_prefix
       )

       df_filtered= df_filtered[df_filtered["id"].isin(cf_recommendations_ids)]
   else:
       # no interactions then clustering
        badge_mapping={
        0:"Budget",
        1:"Mid range",
        2:"Luxury"
    }
   df_clustered=cluster_for_dashboard(df_filtered,numeric_features, n_clusters=3, badge_mapping=badge_mapping)
      
    # convert df to django orm for the serialization and returing responses
   ids = df_filtered["id"].tolist()
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

    