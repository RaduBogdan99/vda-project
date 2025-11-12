from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    # Dashboard principal
    path("admin-panel/", views.admin_dashboard_view, name="admin_dashboard"),
    path("", views.dashboard_view, name="main"),
    path("vehicle/add/", views.vehicle_create_view, name="vehicle_add"),
    path("vehicle/<int:pk>/", views.vehicle_detail_view, name="vehicle_detail"),
    path("vehicle/<int:pk>/edit/", views.vehicle_edit_view, name="vehicle_edit"),
    path("vehicle/<int:pk>/delete/", views.vehicle_delete_view, name="vehicle_delete"),
    path("admin-panel/user/<int:pk>/edit/", views.admin_user_edit_view, name="admin_user_edit"),
    path(
        "admin-panel/user/<int:pk>/delete/", views.admin_user_delete_view, name="admin_user_delete"
    ),
    # URL-uri Documente
    path("vehicle/<int:vehicle_pk>/document/add/", views.document_create_view, name="document_add"),
    path(
        "vehicle/<int:vehicle_pk>/document/<int:pk>/edit/",
        views.document_edit_view,
        name="document_edit",
    ),
    path(
        "vehicle/<int:vehicle_pk>/document/<int:pk>/delete/",
        views.document_delete_view,
        name="document_delete",
    ),
    # URL-uri Mentenanță (Istoric)
    path(
        "vehicle/<int:vehicle_pk>/maintenance/add/",
        views.maintenance_create_view,
        name="maintenance_add",
    ),
    path(
        "vehicle/<int:vehicle_pk>/maintenance/<int:pk>/edit/",
        views.maintenance_edit_view,
        name="maintenance_edit",
    ),
    path(
        "vehicle/<int:vehicle_pk>/maintenance/<int:pk>/delete/",
        views.maintenance_delete_view,
        name="maintenance_delete",
    ),
    # URL-uri Alerte Mentenanță (Reguli)
    path(
        "vehicle/<int:vehicle_pk>/alert/add/",
        views.maintenance_alert_create_view,
        name="maintenance_alert_add",
    ),
    path(
        "vehicle/<int:vehicle_pk>/alert/<int:pk>/edit/",
        views.maintenance_alert_edit_view,
        name="maintenance_alert_edit",
    ),
    path(
        "vehicle/<int:vehicle_pk>/alert/<int:pk>/delete/",
        views.maintenance_alert_delete_view,
        name="maintenance_alert_delete",
    ),
    # URL Export
    path("export/maintenance/", views.export_maintenance_csv, name="export_maintenance_csv"),
]
