from django.db import models, transaction
from django.contrib.auth.models import User
from customer.models import Customer
from decimal import Decimal
from products.models import Product


class SalesOrder(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        CONFIRMED = 'confirmed', 'Confirmed'
        CANCELLED = 'cancelled', 'Cancelled'

    order_number= models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):

        old_status = None
        if self.pk:
            try:
                old_status = SalesOrder.objects.get(pk=self.pk).status
            except SalesOrder.DoesNotExist:
                pass

        super().save(*args, **kwargs)

        # Handle status changes for existing orders
        if old_status and old_status != self.status:
            if self.status == self.Status.CONFIRMED and old_status == self.Status.PENDING:
                self._confirm_order()
            elif self.status == self.Status.CANCELLED and old_status == self.Status.CONFIRMED:
                self._cancel_order()

    @transaction.atomic
    def _confirm_order(self):
        """Confirm order and reduce stock"""
        for line in self.lines.select_for_update().all():
            if line.product.stock < line.qty:
                self.status = self.Status.PENDING
                super().save(update_fields=['status'])
                raise ValueError(
                    f"Not enough stock for {line.product.name}. "
                    f"Available: {line.product.stock}, Requested: {line.qty}"
                )

        for line in self.lines.all():
            line.product.stock -= line.qty
            line.product.save(update_fields=['stock'])

            StockMovementLog.objects.create(
                product=line.product,
                qty=-line.qty,
                user=self.created_by
            )

    @transaction.atomic
    def _cancel_order(self):
        """Cancel order and restore stock"""
        for line in self.lines.select_for_update().all():
            line.product.stock += line.qty
            line.product.save(update_fields=['stock'])

            StockMovementLog.objects.create(
                product=line.product,
                qty=line.qty,
                user=self.created_by
            )

    def update_total(self):
        total = sum(line.line_total for line in self.lines.all())
        self.total_amount = Decimal(total)
        self.save(update_fields=['total_amount'])

    def __str__(self):
        return f"Order {self.order_number} - {self.customer}"


class SalesOrderLine(models.Model):
    order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, related_name='lines')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    @property
    def line_total(self):
        return self.price * self.qty

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.product.selling_price
        super().save(*args, **kwargs)

        if self.order_id:
            self.order.update_total()

    def delete(self, *args, **kwargs):
        order = self.order
        super().delete(*args, **kwargs)
        order.update_total()

    def __str__(self):
        return f"{self.product.name} ({self.qty})"


class StockMovementLog(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_logs')
    qty = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        action = "Added" if self.qty > 0 else "Removed"
        return f"{action} {abs(self.qty)} of {self.product.name} by {self.user}"
