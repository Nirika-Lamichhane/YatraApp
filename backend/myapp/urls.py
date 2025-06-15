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
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),

    path('accounts/', include('accounts.urls')),

    # JWT Token URLs
    path('api/register/', RegisterAPIView.as_view(), name='jwt_register'),  # 🔁 replaces register_view

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh token
    # path('api/token/logout/', TokenBlacklistView.as_view(), name='token_blacklist'),  # Logout (optional)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
