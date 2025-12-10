from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SalesOrderViewSet , StockMovementLogViewSet

router = DefaultRouter()
router.register(r'sales-orders', SalesOrderViewSet, basename='salesorder')
router.register(r'stock-movements', StockMovementLogViewSet, basename='stockmovement')

urlpatterns = [
    path('', include(router.urls)),
]
