from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import SalesOrder
from .serializers import SalesOrderSerializer
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
