from rest_framework.viewsets import ModelViewSet

from apps.products.models import Product
from apps.products.serializers import ProductsSerializer


class ProductsViewSet(ModelViewSet):
    serializer_class = ProductsSerializer
    queryset = Product.objects.all()

