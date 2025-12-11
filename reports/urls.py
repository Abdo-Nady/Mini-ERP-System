from django.urls import path
from .views import export_full_report, dashboard, menu

urlpatterns = [
    path('export_full_report/', export_full_report),
    path('dashboard/', dashboard, name='dashboard'),
    path('menu/', menu, name='menu'),

]
