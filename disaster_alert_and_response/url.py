from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('api/alert/', views.register_user, name='register_user'),
    path('api/users/', views.list_user, name='list_user'),
    path('api/reports/<int:pk>/', views.user_detail, name='report_detail'),
]