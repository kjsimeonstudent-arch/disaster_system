from django.urls import path
from . import views

urlpatterns = [
    # Alerts
    path('api/alerts/', views.get_alerts),
    path('api/alerts/create/', views.create_alert),

    # Reports
    path('api/reports/', views.create_report),

    # Users
    path('api/users/', views.get_users),
]