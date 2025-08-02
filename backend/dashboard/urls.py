from django.urls import path
from . import views

urlpatterns = [
    path('stats/', views.dashboard_stats, name='dashboard_stats'),
    path('activity/', views.dashboard_activity, name='dashboard_activity'),
    path('health/', views.dashboard_health, name='dashboard_health'),
] 