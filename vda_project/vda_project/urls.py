from django.contrib import admin
from django.urls import include, path
from .views import home_view, signup_view, profile_settings_view
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("", home_view, name="home"),
    path("admin/", admin.site.urls),
    # URL-uri de Autentificare
    path("accounts/signup/", signup_view, name="signup"),
    path("accounts/profile/", profile_settings_view, name="profile_settings"),
    path("accounts/", include("django.contrib.auth.urls")),
    # URL-uri Dashboard (Interfața utilizatorului)
    path("dashboard/", include("dashboard.urls")),
    # URL-uri API
    path("api-auth/", include("rest_framework.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/v1/", include("vda_project.api_urls")),  # Router-ul API central
]

# Servește fișierele media (atașamentele) doar în modul DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
