from django.db.models import Q
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from recipes.models import Recipe, Ingredient, CookingStep
from recipes.serializers import RecipeSearchSerializer, IngredientsSerializer, StagesSerializer, RecipeSerializer


class RecipesSearcher(ViewSet):
    def list(self, request: Request, *args, **kwargs):
        products_ids = request.query_params.get("products")

        if not products_ids:
            response = RecipeSearchSerializer(Recipe.objects.all(), many=True)
            return Response(response.data)

        ids = tuple(products_ids.split(','))

        query = """
SELECT r.*,
       count(i.product_id)
FROM recipes_recipe r
LEFT JOIN recipes_ingredient AS i ON i.recipe_id = r.id
WHERE i.product_id in %s
GROUP BY r.id,
         r.title
ORDER BY count(i.product_id) DESC
        """

        recipes = Recipe.objects.raw(query, [ids])
        serialized = RecipeSearchSerializer(recipes, many=True, context={"count": len(ids)})

        return Response({"response": serialized.data})


class RecipesViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        recipe_serializer = RecipeSerializer(instance)

        ingredients = Ingredient.objects.filter(recipe__id=instance.id).all()
        ingredient_serializer = IngredientsSerializer(ingredients, many=True)

        return Response({"recipe": recipe_serializer.data,
                         "ingredients": ingredient_serializer.data})

    def update(self, request, *args, **kwargs) -> Response:
        pass

    def create(self, request: Request, *args, **kwargs) -> Response:  # ingredients, recipe
        ingredients = request.data.get("ingredients", [])
        recipe = request.data.get("recipe", {})

        new_recipe = RecipeSerializer(data=recipe)
        if not new_recipe.is_valid():
            raise ValidationError({"recipe": new_recipe.errors})

        new_recipe.save()

        new_ingredients = IngredientsSerializer(data=ingredients, many=True, context={"recipe": new_recipe.instance})
        if not new_ingredients.is_valid():
            raise ValidationError({"ingredients": new_ingredients.errors})

        new_ingredients.save()

        return Response({
            "recipe": new_recipe.data,
            "ingredients": new_ingredients.data
        }, status=201)


class StagesViewSet(ModelViewSet):
    serializer_class = StagesSerializer

    lookup_field = "step"

    def get_serializer_context(self):
        default_context = super().get_serializer_context()
        default_context["recipe"] = self.get_recipe(raise_exception=False)
        return default_context

    def get_recipe(self, *, raise_exception):
        recipe = Recipe.objects.filter(id=self.kwargs["recipe_id"]).first()

        if raise_exception and not recipe:
            raise NotFound()

        return recipe

    def get_queryset(self):
        recipe = self.get_recipe(raise_exception=True)
        return CookingStep.objects.filter(recipe=recipe).order_by("step")
