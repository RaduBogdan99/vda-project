from rest_framework.routers import DefaultRouter
from .views import VehicleViewSet

# Creăm un router
router = DefaultRouter()
# Înregistrăm ViewSet-ul nostru. DRF se va ocupa de URL-uri
# 'vehicles' va fi baza URL-ului (ex: /api/v1/vehicles/)
router.register(r"vehicles", VehicleViewSet, basename="vehicle")

# URL-urile API sunt acum generate de router
urlpatterns = router.urls
