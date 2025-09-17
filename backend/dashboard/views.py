# dashboard/views.py

# ------------------- DRF and Django imports -------------------
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

# ------------------- Models and serializers -------------------
from .models import Place, Hotel, Food, Activity, Favorite, Comment
from .serializers import (
    PlaceSerializer, HotelSerializer, FoodSerializer, ActivitySerializer,
    FavoriteSerializer, CommentSerializer
)

# ------------------- ML imports from db_loader -------------------
from .ml.db_loader import (
    load_all_data,
    create_user_item_matrix,
    get_recommendations,
    fetch_items_from_ids
)

# ------------------- CRUD API ViewSets -------------------

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
        # Automatically assigns the logged-in user to the favorite
        serializer.save(user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically assigns the logged-in user to the comment
        serializer.save(user=self.request.user)


# ------------------- Recommendation API -------------------

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommend_view(request):
    """
    Generates initial personalized recommendations for the logged-in user
    using collaborative filtering on user interactions.
    """

    user_id = request.user.id  # Get logged-in user's ID

    # Step 1: Load all necessary tables from PostgreSQL into pandas DataFrames
    destinations, destination_types, places, activities, foods, hotels, user_interactions = load_all_data()

    # Step 2: Create a user-item interaction matrix
    # Rows = users, Columns = unique items (combination of content_type_id + object_id)
    user_item_matrix = create_user_item_matrix(user_interactions)

    # Step 3: Generate recommended item IDs for this user
    recommended_item_ids = get_recommendations(user_id, user_item_matrix, top_n=5)

    # Step 4: Fetch actual item objects (places, hotels, foods, activities) from recommended IDs
    recommended_items = fetch_items_from_ids(
        recommended_item_ids,
        places=places,
        hotels=hotels,
        foods=foods,
        activities=activities
    )

    # Step 5: Serialize each type of item for API response
    serializer = {
        'places': PlaceSerializer(recommended_items.get('places', []), many=True).data,
        'hotels': HotelSerializer(recommended_items.get('hotels', []), many=True).data,
        'foods': FoodSerializer(recommended_items.get('foods', []), many=True).data,
        'activities': ActivitySerializer(recommended_items.get('activities', []), many=True).data,
    }

    # Step 6: Return recommendations as JSON
    return Response({
        "user_id": user_id,
        "recommendations": serializer
    }, status=200)
