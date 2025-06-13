from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import DestinationType, Destination, CustomUser
from .serializers import DestinationTypeSerializer, DestinationSerializer, CustomUserSerializer


# --- User Authentication Views ---

@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if CustomUser.objects.filter(username=username).exists():
            return JsonResponse({'status': 'error', 'message': 'Username already exists'})

        user = CustomUser.objects.create_user(username=username, email=email, password=password)
        user.save()
        return JsonResponse({'status': 'success', 'message': 'User registered successfully'})

    return JsonResponse({'status': 'error', 'message': 'Only POST method allowed'})


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            return JsonResponse({'status': 'success', 'message': 'Login successful'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid credentials'})

    return JsonResponse({'status': 'error', 'message': 'Only POST method allowed'})


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
