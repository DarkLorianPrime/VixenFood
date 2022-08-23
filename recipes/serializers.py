from rest_framework.serializers import ModelSerializer

from recipes.models import Recipe, RecipeIngredients


class IngredientsRecipeSerializer(ModelSerializer):
    class Meta:
        model = RecipeIngredients
        fields = "__all__"


class RecipeSerializer(ModelSerializer):
    class Meta:
        model = Recipe
        fields = "__all__"
