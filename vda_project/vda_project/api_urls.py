from rest_framework.routers import DefaultRouter
from vehicles.views import VehicleViewSet
from documents.views import DocumentViewSet
from maintenance.views import MaintenanceViewSet

# Acesta este router-ul nostru API principal
router = DefaultRouter()

# Înregistrăm toate ViewSet-urile noastre
router.register(r'vehicles', VehicleViewSet, basename='vehicle')
router.register(r'documents', DocumentViewSet, basename='document')
router.register(r'maintenance', MaintenanceViewSet, basename='maintenance')

urlpatterns = router.urls