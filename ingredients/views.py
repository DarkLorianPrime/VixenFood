from rest_framework.viewsets import ModelViewSet

from ingredients.models import Ingredient
from ingredients.serializers import IngredientsSerializer


class IngredientsViewSet(ModelViewSet):
    serializer_class = IngredientsSerializer
    queryset = Ingredient.objects.all()

