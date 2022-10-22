from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from recipes.models import Recipe, Ingredient, CookingStep


class IngredientsSerializer(ModelSerializer):
    def create(self, validated_data: dict):
        if validated_data.get("count") is None and validated_data.get("grams") is None:
            raise ValidationError({"count": ["One of this parameters will be not null"],
                                   "grams": ["One of this parameters will be not null"]})
        return Ingredient.objects.create(**validated_data)

    class Meta:
        model = Ingredient
        fields = "__all__"


# class RecipeSearchSerializer(ModelSerializer):
#     complete_match = SerializerMethodField(method_name="is_complete")
#
#     def is_complete(self, model):
#         return None if not self.context.get("count") else self.context["count"] == model.count
#
#     def create(self, validated_data: dict):
#         return Recipe.objects.create(**validated_data)
#
#     class Meta:
#         model = Recipe
#         fields = ("title", "difficulty", "cooking_time", "complete_match")

class RecipeSerializer(ModelSerializer):

    def create(self, validated_data: dict):
        return Recipe.objects.create(**validated_data)

    class Meta:
        model = Recipe
        fields = ("title", "difficulty", "cooking_time")


class RecipeSearchSerializer(RecipeSerializer):
    complete_match = SerializerMethodField(method_name="is_complete")

    def is_complete(self, model):
        return None if not self.context.get("count") else self.context["count"] == model.count

    class Meta:
        model = Recipe
        fields = ("title", "difficulty", "cooking_time", "complete_match")


class StagesSerializer(ModelSerializer):

    def create(self, validated_data):
        if CookingStep.objects.filter(recipe_id=validated_data["recipe_id"], step=validated_data["step"]).exists():
            raise ValidationError({"step": ["This step for this recipe already exists!"]})

        return CookingStep.objects.create(**validated_data)

    class Meta:
        model = CookingStep
        fields = "__all__"
