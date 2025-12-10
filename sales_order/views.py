from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import SalesOrder , StockMovementLog
from .serializers import SalesOrderSerializer ,StockMovementLogSerializer
from .permissions import IsAdminOrSalesUserCreateOnly


class SalesOrderViewSet(viewsets.ModelViewSet):
    queryset = SalesOrder.objects.all()
    serializer_class = SalesOrderSerializer
    permission_classes = [IsAuthenticated & IsAdminOrSalesUserCreateOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        order = serializer.save()
        if order.status == order.Status.CONFIRMED:
            order.confirm_order()
        elif order.status == order.Status.CANCELLED:
            order.cancel_order()


class StockMovementLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StockMovementLog.objects.all().order_by('-timestamp')
    serializer_class = StockMovementLogSerializer
    permission_classes = [IsAuthenticated]