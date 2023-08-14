from rest_framework.viewsets import ModelViewSet

from products.models import Product
from products.serializers import ProductsSerializer


class ProductsViewSet(ModelViewSet):
    serializer_class = ProductsSerializer
    queryset = Product.objects.all()

