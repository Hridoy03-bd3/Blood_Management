from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('accounts/', include('accounts.urls')),
    path('', include('blood.urls')),  # Custom app URLs (including /admin/users/, etc.) must come before Django admin
    path('admin/', admin.site.urls),  # Django admin site
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
