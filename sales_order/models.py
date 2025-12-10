from django.db import models
from django.contrib.auth.models import User
from customer.models import Customer
from decimal import Decimal
from products.models import Product
# Create your models here.

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


    def confirm_order(self):
        if self.status == self.Status.PENDING:
            for line in self.lines.all():
                if line.product.stock < line.qty:
                    raise ValueError(f"Not enough stock for {line.product.name}")

            for line in self.lines.all():
                line.product.stock -= line.qty
                line.product.save()
            self.status = self.Status.CONFIRMED
            self.save()

    def cancel_order(self):
        if self.status == self.Status.CONFIRMED:
            for line in self.lines.all():
                line.product.stock += line.qty
                line.product.save()
            self.status = self.Status.CANCELLED
            self.save()

    def update_total(self):
        total = sum(line.line_total for line in self.lines.all())
        self.total_amount = Decimal(total)
        self.save()

    def __str__(self):
        return f"Order {self.order_number} - {self.customer}"

class SalesOrderLine(models.Model):
    order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, related_name='lines')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def line_total(self):
        return self.price * self.qty

    def __str__(self):
        return f"{self.product.name} ({self.qty})"
