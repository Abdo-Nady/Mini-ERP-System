from rest_framework import viewsets ,filters
from .models import Product
from .serializers import ProductSerializer
from .permissions import IsAdminOrReadOnly
from rest_framework.pagination import PageNumberPagination


class ProductPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['sku', 'name', 'category',]
    pagination_class = ProductPagination

    def get_queryset(self):
        qs = super().get_queryset()
        # filter by category
        category = self.request.query_params.get('category')
        if category:
            qs = qs.filter(category=category)
        return qs
