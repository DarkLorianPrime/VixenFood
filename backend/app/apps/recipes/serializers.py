from django.db.models import Q
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField, CharField
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from apps.products.models import Product
from apps.recipes.models import Recipe, Ingredient, CookingStep


class IngredientsSerializer(ModelSerializer):
    recipe = PrimaryKeyRelatedField(default=None, queryset=Recipe.objects.all(), write_only=True)
    product = PrimaryKeyRelatedField(queryset=Product.objects.all())
    product_name = CharField(source="product.name", read_only=True)

    def validate(self, attrs):
        ingredient = attrs.get("count") or attrs.get("grams")

        if ingredient:
            return attrs

        raise ValidationError({"count": ["One of  this parameters will be not null"],
                               "grams": ["One of  this parameters will be not null"]})

    def validate_recipe(self, _):
        return self.context["recipe"]

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
    class Meta:
        model = Recipe
        fields = ("id", "title", "difficulty", "cooking_time")


class RecipeSearchSerializer(RecipeSerializer):
    complete_match = SerializerMethodField(method_name="is_complete")

    def is_complete(self, model):
        return None if not self.context.get("count") else self.context["count"] == model.count

    class Meta:
        model = Recipe
        fields = ("title", "difficulty", "cooking_time", "complete_match")


class StagesSerializer(ModelSerializer):
    recipe = PrimaryKeyRelatedField(default=None, queryset=Recipe.objects.all(), write_only=True)

    def validate_recipe(self, _):
        return self.context["recipe"]

    def validate(self, attrs):
        return attrs

    def update(self, instance: CookingStep, validated_data):
        exists_instance = CookingStep.objects.filter(~Q(id=instance.id),
                                                     step=validated_data["step"],
                                                     recipe=instance.recipe).first()
        if exists_instance:
            instance.swap_step(exists_instance)

        return super().update(instance, validated_data)

    class Meta:
        model = CookingStep
        exclude = ["id"]
