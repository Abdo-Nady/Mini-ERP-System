from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
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

    # مش محتاج perform_update تاني!
    # الـ model هيعمل كل حاجة أوتوماتيك

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """Shortcut to confirm order"""
        order = self.get_object()
        if order.status != SalesOrder.Status.PENDING:
            return Response(
                {'error': 'Order is not pending'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            order.status = SalesOrder.Status.CONFIRMED
            order.save()
            return Response({'status': 'Order confirmed successfully'})
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Shortcut to cancel order"""
        order = self.get_object()
        if order.status != SalesOrder.Status.CONFIRMED:
            return Response(
                {'error': 'Only confirmed orders can be cancelled'},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = SalesOrder.Status.CANCELLED
        order.save()
        return Response({'status': 'Order cancelled successfully'})


class StockMovementLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StockMovementLog.objects.all()
    serializer_class = StockMovementLogSerializer
    permission_classes = [IsAuthenticated]