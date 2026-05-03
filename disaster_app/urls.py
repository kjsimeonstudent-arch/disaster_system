from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('api/auth/register/', views.register_user, name='register'),
    path('api/auth/login/', views.login_user, name='login'),

    # Alerts (Disasters)
    path('api/alerts/', views.get_alerts, name='get_alerts'),
    path('api/alerts/create/', views.create_alert, name='create_alert'),

    # Requests
    path('api/requests/', views.get_requests, name='get_requests'),
    path('api/requests/create/', views.create_request, name='create_request'),
    path('api/requests/<int:request_id>/', views.get_request_detail, name='get_request_detail'),

    # Reports
    path('api/reports/', views.get_reports, name='get_reports'),
    path('api/reports/create/', views.create_report, name='create_report'),
    path('api/reports/<int:report_id>/', views.get_report_detail, name='get_report_detail'),
]