from rest_framework import viewsets
from .models import Customer
from .serializers import CustomerSerializer
from .permissions import IsAdminOrCreateOnly
# Create your views here.




class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminOrCreateOnly]