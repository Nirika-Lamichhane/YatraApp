# dashboard/views.py

# ------------------- DRF imports -------------------
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

# ------------------- ML helpers -------------------
from .ml.dataLoader import (
    load_all_data,
    create_user_item_matrix,
    get_recommendations,
    fetch_items_from_ids
)

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

    # Step 1: Load all necessary tables into pandas DataFrames
    destinations, destination_types, places, activities, foods, hotels, user_interactions = load_all_data()

    # Step 2: Create user-item interaction matrix
    user_item_matrix = create_user_item_matrix(user_interactions)
    # This matrix has:
    # Rows = users
    # Columns = items (Place, Hotel, Food, Activity)
    # Value = 1 if favorite, 0.5 if comment (example)

    # Step 3: Get top recommended item IDs for this user
    recommended_item_ids = get_recommendations(user_id, user_item_matrix, top_n=5)
    # Example output: ['place_12', 'hotel_3', 'food_5', ...]

    # Step 4: Convert item IDs to actual Django objects
    recommended_items = fetch_items_from_ids(
        recommended_item_ids,
        places=places,
        hotels=hotels,
        foods=foods,
        activities=activities
    )

    # Step 5: Serialize each type of item
    serializer = {
        'places': PlaceSerializer(recommended_items.get('places', []), many=True).data,
        'hotels': HotelSerializer(recommended_items.get('hotels', []), many=True).data,
        'foods': FoodSerializer(recommended_items.get('foods', []), many=True).data,
        'activities': ActivitySerializer(recommended_items.get('activities', []), many=True).data,
    }

    # Step 6: Return JSON response
    return Response({
        "user_id": user_id,
        "recommendations": serializer
    }, status=200)
