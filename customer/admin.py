from django.contrib import admin
from .models import Customer

# Register your models here.


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name','phone' ,'email' , 'address' , 'opening_balance']
    search_fields = ['name', 'email']
