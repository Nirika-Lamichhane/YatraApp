from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, get_user_model
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import DestinationType, Destination, CustomUser
from .serializers import DestinationTypeSerializer, DestinationSerializer, CustomUserSerializer

import uuid

User = get_user_model()


# --- User Authentication Views ---

@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')


        profile_photo = request.FILES.get('profile_photo')
        citizenship_photo = request.FILES.get('citizenship_photo')

        if not username or not email or not password:
            return JsonResponse({'status': 'error', 'message': 'Username, email, and password are required.'})

        if not profile_photo:
            return JsonResponse({'status': 'error', 'message': 'Profile photo is required.'})

        if not citizenship_photo:
            return JsonResponse({'status': 'error', 'message': 'Citizenship photo is required.'})

        if CustomUser.objects.filter(username=username).exists():
            return JsonResponse({'status': 'error', 'message': 'Username already exists.'})

        user = CustomUser.objects.create_user(username=username, email=email, password=password, phone_number=phone_number)

        # Save uploaded files
        profile_filename = f"profile_photos/{uuid.uuid4().hex}_{profile_photo.name}"
        user.profile_photo.save(profile_filename, profile_photo)

        citizen_filename = f"citizenship_photos/{uuid.uuid4().hex}_{citizenship_photo.name}"
        user.citizenship_photo.save(citizen_filename, citizenship_photo)

        user.save()

        return JsonResponse({'status': 'success', 'message': 'User registered successfully.'})

    return JsonResponse({'status': 'error', 'message': 'Only POST method allowed.'})


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
      

        user = authenticate(username=username, password=password)
        if user is not None:
            return JsonResponse({
                'status': 'success',
                'message': 'Login successful.',
                'user': {
                    'username': user.username,
                    'email': user.email,
                    'profile_photo': user.profile_photo.url if user.profile_photo else None,
                    'citizenship_photo': user.citizenship_photo.url if user.citizenship_photo else None,
                }
            })
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid credentials.'})

    return JsonResponse({'status': 'error', 'message': 'Only POST method allowed.'})


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
