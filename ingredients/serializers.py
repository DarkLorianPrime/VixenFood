from rest_framework.serializers import ModelSerializer

from ingredients.models import Ingredient


class IngredientsSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"
