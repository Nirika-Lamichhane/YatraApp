from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import home  # ✅ Import the view
from accounts.views import RegisterAPIView # ✅ Import the registration view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,     
    TokenVerifyView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),

    path('accounts/', include('accounts.urls')),


    # Include the accounts app URLs
    path('api/', include('accounts.urls')),  # ✅ Include the accounts app URLs
    # JWT Token URLs
    path('api/register/', RegisterAPIView.as_view(), name='jwt_register'),  # 🔁 replaces register_view

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh token
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),  # Verify token check if the token is valid or not from flutter
    path('api/token/logout/', TokenBlacklistView.as_view(), name='token_blacklist'),  # Logout (optional) this removes all fresh token after logout
    
    path('api/', include('dashboard.chatbot.urls')),  # now your chatbot API is at /api/chatbot/

    path('api/dashboard/', include('dashboard.urls')),  # Include the dashboard app URLs
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
