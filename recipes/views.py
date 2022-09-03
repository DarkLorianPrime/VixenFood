from django.db import connection
from django.db.models import Q, Index, Count
from django.db.models.functions import Lower
from django.http import HttpResponse
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from recipes.models import Recipe, Ingredient
from recipes.serializers import RecipeSerializer, IngredientsSerializer


class RecipesSearcher(ViewSet):
    def list(self, request: Request, *args, **kwargs):
        products_ids = request.query_params.get("products")

        if not products_ids:
            response = RecipeSerializer(Recipe.objects.all(), many=True)
            return Response(response.data)

        query = """select r.*, count(i.product_id) from recipes_recipe r 
        left join recipes_ingredient as i on i.recipe_id = r.id
        where i.product_id in %s
        group by r.id, r.title
        order by count(i.product_id) desc"""

        recipe = Recipe.objects.raw(query, [tuple(products_ids.split(','))])

        count_products = len(products_ids.split(","))
        exact = [i for i in recipe if i.count == count_products]
        additional = [i for i in recipe if i.count != count_products]

        response_exact = RecipeSerializer(exact, many=True)
        response_additional = RecipeSerializer(additional, many=True)

        return Response({"response": {"exact": response_exact.data, "additional": response_additional.data}})


class RecipesViewSet(ModelViewSet):
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

        # ingredients_id = [i["ingredient"] for i in ingredients]
        # calories_count = Ingredient.objects.filter(id__in=ingredients_id).aggregate(calorie=Sum("calorie"))["calorie"]
        # recipe["calories"] = calories_count

        recipe = RecipeSerializer(data=recipe)
        recipe.is_valid(raise_exception=True)
        recipe.save()

        for i in ingredients:
            i["recipe"] = recipe["id"].value

        serializer = IngredientsSerializer(data=ingredients, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"response": [recipe.data, serializer.data]}, status=201)
