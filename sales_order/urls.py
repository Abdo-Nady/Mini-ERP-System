from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SalesOrderViewSet

router = DefaultRouter()
router.register(r'sales-orders', SalesOrderViewSet, basename='salesorder')

urlpatterns = [
    path('', include(router.urls)),
]
