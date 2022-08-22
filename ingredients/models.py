from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    calorie = models.IntegerField()


class RecipeIngredients(models.Model):
    ingredient = models.ForeignKey("Ingredient", on_delete=models.CASCADE)
    recipe = models.ForeignKey("recipes.Recipe", on_delete=models.CASCADE)
    required = models.BooleanField(default=False)
    grams = models.IntegerField()

    class Meta:
        db_table = "recipe__ingredients"
