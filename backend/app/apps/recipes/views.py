from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from apps.recipes.models import Recipe
from apps.recipes.repositories import RecipeRepository, IngredientRepository, StageRepository
from apps.recipes.serializers import RecipeSearchSerializer, IngredientsSerializer, StagesSerializer, RecipeSerializer

recipe_repository = RecipeRepository()
ingredient_repository = IngredientRepository()
stage_repository = StageRepository()


class RecipesSearcher(ViewSet):
    def list(self, request: Request, *args, **kwargs):
        products_string = request.query_params.get("products")

        if not products_string:
            response = RecipeSerializer(recipe_repository.get_all(), many=True)
            return Response(response.data)

        products_ids = tuple(set(products_string.split(',')))
        products_count = len(products_ids)

        recipes = recipe_repository.search_by_ids(products_ids)
        serialized = RecipeSearchSerializer(recipes, many=True, context={"count": products_count})

        sorted_data = sorted(serialized.data, key=lambda x: x["complete_match"], reverse=True)

        return Response(sorted_data)


class IngredientsViewSet(ModelViewSet):
    search_fields = ("product__name", "required", "grams", "count")
    ordering_fields = ("required", "grams", "count")
    queryset = ingredient_repository.get_all()
    serializer_class = IngredientsSerializer

    def get_recipe(self):
        recipe = recipe_repository.get_recipe(self.kwargs["recipe_id"])

        return recipe

    def get_queryset(self):
        recipe = self.get_recipe()

        if not recipe:
            raise NotFound()

        return ingredient_repository.get_ingredients(recipe=recipe)


class RecipesViewSet(ModelViewSet):
    search_fields = ("title", "difficulty", "cooking_time")
    ordering_fields = ("id", "cooking_time")
    queryset = recipe_repository.get_all()
    serializer_class = RecipeSerializer

    def retrieve(self, request, *args, **kwargs):
        instance: Recipe = self.get_object()
        recipe_serializer = RecipeSerializer(instance)

        # получаем в том числе данные о ингредиентах, чтобы вывести исчерпывающую информацию
        ingredients = ingredient_repository.get_ingredients(recipe__id=instance.id)
        ingredient_serializer = IngredientsSerializer(ingredients, many=True)

        return Response({"recipe": recipe_serializer.data,
                         "ingredients": ingredient_serializer.data})

    def create(self, request: Request, *args, **kwargs) -> Response:  # ingredients, recipe
        ingredients_object = request.data.get("ingredients", [])
        recipe_object = request.data.get("recipe", {})

        recipe = RecipeSerializer(data=recipe_object)
        # Кастомная проверка валидности, для вывода блока, в котором неправильно заполнены данные

        if not recipe.is_valid():
            raise ValidationError({"recipe": recipe.errors})

        recipe.save()

        ingredients = IngredientsSerializer(data=ingredients_object, many=True, context={"recipe": recipe.instance})

        # Кастомная проверка валидности, для вывода блока, в котором неправильно заполнены данные
        if not ingredients.is_valid():
            raise ValidationError({"ingredients": ingredients.errors})

        ingredients.save()

        return Response({
            "recipe": recipe.data,
            "ingredients": ingredients.data
        }, status=201)


class StagesViewSet(ModelViewSet):
    ordering_fields = ("step",)
    serializer_class = StagesSerializer
    lookup_field = "step"

    def get_serializer_context(self):
        default_context = super().get_serializer_context()
        # Добавляем recipe в context, чтобы не переопределять update и create
        default_context["recipe"] = self.get_recipe()
        return default_context

    def get_recipe(self):
        recipe = recipe_repository.get_recipe(self.kwargs["recipe_id"])

        return recipe

    def get_queryset(self):
        recipe = self.get_recipe()

        if not recipe:
            raise NotFound()

        return stage_repository.get_ordered_stages(recipe)
