from typing import Any, Dict

from django.db.models import Q
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField, CharField
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from apps.products.repositories import ProductRepository
from apps.recipes.models import CookingStep, Recipe, Ingredient
from apps.recipes.repositories import RecipeRepository, IngredientRepository, StageRepository

recipe_repository = RecipeRepository()
ingredient_repository = IngredientRepository()
stage_repository = StageRepository()
product_repository = ProductRepository()


class IngredientsSerializer(ModelSerializer):
    recipe = PrimaryKeyRelatedField(default=None, queryset=recipe_repository.get_all(), write_only=True)
    product = PrimaryKeyRelatedField(queryset=product_repository.get_all())
    product_name = CharField(source="product.name", read_only=True)

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        ingredient = attrs.get("count") or attrs.get("grams")

        if self.context["request"].method != "POST" or ingredient:
            return attrs

        raise ValidationError({"count": ["One of this parameters will be not null"],
                               "grams": ["One of this parameters will be not null"]})

    def validate_recipe(self, _) -> Recipe:
        return self.context["recipe"]

    class Meta:
        model = Ingredient
        fields = "__all__"


class RecipeSerializer(ModelSerializer):
    class Meta:
        model = Recipe
        fields = ("id", "title", "difficulty", "cooking_time")


class RecipeSearchSerializer(RecipeSerializer):
    complete_match = SerializerMethodField(method_name="is_complete")

    def is_complete(self, model):
        # проверяет, совпадает ли количество
        # переданных ингредиентов и количество ингредиентов в модели
        products_count = self.context.get("count")
        return products_count == model.ingredients_count

    class Meta:
        model = Recipe
        fields = ("id", "title", "difficulty", "cooking_time", "complete_match")


class StagesSerializer(ModelSerializer):
    recipe = PrimaryKeyRelatedField(default=None, queryset=recipe_repository.get_all(), write_only=True)

    def validate_recipe(self, _) -> Recipe:
        return self.context["recipe"]

    def update(self, instance: CookingStep, validated_data: Dict[str, Any]) -> CookingStep:
        exists_instance = stage_repository.get_stage(~Q(id=instance.id),
                                                     step=validated_data["step"],
                                                     recipe=instance.recipe)
        if exists_instance:
            instance.swap_step(exists_instance)

        return super().update(instance, validated_data)

    class Meta:
        model = CookingStep
        exclude = ("id",)
