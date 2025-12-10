from django.urls import path
from .views import export_full_report

urlpatterns = [
    path('export_full_report/', export_full_report),
]