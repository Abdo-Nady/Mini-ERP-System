from django.urls import path
from .views import export_full_report , dashboard

urlpatterns = [
    path('export_full_report/', export_full_report),
    path('dashboard/',dashboard,name='dashboard')
]