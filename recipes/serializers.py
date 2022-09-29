from django.conf.locale import en
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from recipes.models import Recipe, Ingredient


class IngredientsSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"


class RecipeSerializer(ModelSerializer):
    complete_match = SerializerMethodField(method_name="is_complete")

    def is_complete(self, model):
        if not self.context.get("count"):
            return None
        return self.context["count"] == model.count

    def create(self, validated_data):
        return Recipe.objects.create(**validated_data)

    class Meta:
        model = Recipe
        fields = ("title", "difficulty", "cooking_time", "complete_match")
