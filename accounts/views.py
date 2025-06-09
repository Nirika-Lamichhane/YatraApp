from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.files.base import ContentFile

from django.core.files.storage import default_storage

import uuid

@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        profile_photo = request.FILES.get('profile_photo')
        citizenship_photo = request.FILES.get('citizenship_photo')

        if User.objects.filter(username=username).exists():
            return JsonResponse({'status': 'error', 'message': 'Username already exists'})

        user = User.objects.create_user(username=username, email=email, password=password)

        if profile_photo:
            profile_filename = f"profile_photos/{uuid.uuid4().hex}_{profile_photo.name}"
            default_storage.save(profile_filename, ContentFile(profile_photo.read()))

        if citizenship_photo:
            citizen_filename = f"citizenship_photos/{uuid.uuid4().hex}_{citizenship_photo.name}"
            default_storage.save(citizen_filename, ContentFile(citizenship_photo.read()))
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
