# Отделяем бизнес-логику от обычной
from typing import Tuple, Any

from django.db.models import QuerySet

from apps.recipes.models import Ingredient, Recipe, CookingStep
from core.abstracts.repositories import AbstractRepository


class RecipeRepository(AbstractRepository):
    def __init__(self):
        self.model = Recipe

    def get_recipe(self, recipe_id: int) -> Recipe:
        return self.model.objects.filter(id=recipe_id).first()

    def search_by_ids(self, products_ids: Tuple[Any]):
        query = """
SELECT  
  r.*, 
  COUNT(i.product_id) AS ingredients_count 
FROM 
  recipes_recipe r 
  LEFT JOIN recipes_ingredient AS i ON i.product_id IN %s 
WHERE 
  i.recipe_id = r.id 
GROUP BY 
  r.id, 
  r.title;
        """
# Поиск всех рецептов с переданными product_id, а так же количества их ингредиентов
        recipes = Recipe.objects.raw(query, [products_ids])
        return recipes


class IngredientRepository(AbstractRepository):
    def __init__(self):
        self.model = Ingredient

    def get_ingredients(self, **kwargs) -> QuerySet:
        return self.model.objects.filter(**kwargs).all()


class StageRepository(AbstractRepository):
    def __init__(self):
        self.model = CookingStep

    def get_ordered_stages(self, recipe: Recipe) -> QuerySet:
        return self.model.objects.filter(recipe=recipe).order_by("step")

    def get_stage(self, *args, **kwargs) -> CookingStep:
        return self.model.objects.filter(*args, **kwargs).first()
