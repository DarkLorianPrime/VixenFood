from rest_framework.serializers import ModelSerializer

from recipes.models import Recipe, Ingredient


class IngredientsSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"


class RecipeSerializer(ModelSerializer):
    class Meta:
        model = Recipe
        fields = "__all__"
