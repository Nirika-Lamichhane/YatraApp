from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from .models import DestinationType, Destination, CustomUser
from .serializers import DestinationTypeSerializer, DestinationSerializer, CustomUserSerializer

import uuid



User = get_user_model()

from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the homepage!")



# --- User Registration View using DRF and JWT tokens ---

class RegisterAPIView(APIView):
    permission_classes = [permissions.AllowAny]  # anyone can register

    def post(self, request):
        data = request.data.copy()  # mutable copy of incoming data

        # Validate required files in request.FILES
        profile_photo = request.FILES.get('profile_photo')

        if not profile_photo:
            return Response({'profile_photo': ['This field is required.']}, status=status.HTTP_400_BAD_REQUEST)
        

        # Save the files to request.data for serializer
        data['profile_photo'] = profile_photo

        serializer = CustomUserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()

            # Create JWT tokens for the new user
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': CustomUserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# --- Destination APIs using DRF ---

@api_view(['GET'])
def get_destination_types(request):
    types = DestinationType.objects.all()
    serializer = DestinationTypeSerializer(types, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_destinations_by_types(request):
    type_ids = request.query_params.getlist('type_ids')  # e.g. ?type_ids=1&type_ids=2
    destinations = Destination.objects.filter(type__id__in=type_ids)
    serializer = DestinationSerializer(destinations, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_favorite_destinations(request):
    user = request.user
    destination_ids = request.data.get('destination_ids', [])
    destinations = Destination.objects.filter(id__in=destination_ids)
    user.favorites.set(destinations)
    user.save()
    return Response({"message": "Favorites updated successfully"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_favorites(request):
    user = request.user
    serializer = CustomUserSerializer(user)
    return Response(serializer.data)


# this is the view of recommendation system, we can change it later with actual ML logic
@api_view(['POST'])
@permission_classes([IsAuthenticated])  # 👈 ensures the user must be logged in
def recommend_view(request):
    user = request.user  # 👈 Gets the logged-in user

    # You can add ML logic here later using the user profile
    serializer = CustomUserSerializer(user)
    
    return Response({
        "user": serializer.data,
        "recommendations": ["Pokhara", "Mustang", "Bandipur"]  # dummy for now
    }, status=status.HTTP_200_OK)
