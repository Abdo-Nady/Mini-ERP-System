from django.db import models


# Create your models here.


class Customer(models.Model):
    customer_code = models.CharField(
        max_length=50,
        unique=True,
        editable=False,
        null=True,
        blank=True
    )
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    address = models.TextField()

    opening_balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)

        if not self.customer_code:
            self.customer_code = f"CUST-{self.pk:05d}"
            super().save(update_fields=['customer_code'])
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer_code} - {self.name}"
