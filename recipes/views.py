from django.core import serializers
from django.db.models import Q, Sum
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet

from ingredients.models import Ingredient
from ingredients.serializers import IngredientsSerializer
from recipes.models import RecipeIngredients, Recipe
from recipes.serializers import IngredientsRecipeSerializer, RecipeSerializer


class Recipes(ModelViewSet):
    def list(self, request, *args, **kwargs) -> HttpResponse:
        recipes = Recipe.objects.all()
        for i in recipes:
            print(i.cooking_time)
        recipes_serialize = RecipeSerializer(recipes, many=True)
        return Response(recipes_serialize.data)

    def update(self, request, *args, **kwargs) -> HttpResponse:
        pass

    def create(self, request: Request, *args, **kwargs) -> HttpResponse:  # ingredients, weights, required
        ingredients = request.data.get("ingredients")
        recipe = request.data.get("recipe")

        if not ingredients:
            return Response(data="In JSON need dict field \"ingredients\"", status=400)

        if not recipe:
            return Response(data="In JSON need dict field \"recipe\"", status=400)

        # query = Q()
        # for i in ingredients:
        #     query |= Q(id=i["ingredient"])
        # calories_count = Ingredient.objects.filter(query).aggregate(calories=Sum("calorie"))

        ingredients_id = [i["ingredient"] for i in ingredients]
        calories_count = Ingredient.objects.filter(id__in=ingredients_id).aggregate(calorie=Sum("calorie"))["calorie"]
        recipe["calories"] = calories_count

        recipe = RecipeSerializer(data=recipe)
        recipe.is_valid(raise_exception=True)
        recipe.save()

        for i in ingredients:
            i["recipe"] = recipe["id"].value

        serializer = IngredientsRecipeSerializer(data=ingredients, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"response": [recipe.data, serializer.data]}, status=201)
