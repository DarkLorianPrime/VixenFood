from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from products.models import Product


class ProductsSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

    def validate_name(self, name):
        if not Product.objects.filter(name=name).exists():
            return name

        raise ValidationError("this name already exists")

