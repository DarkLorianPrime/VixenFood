from django.db import models


class Difficult(models.Model):
    difficulties = (
        ('Noob', 'Noob'),
        ('Master', 'Master'),
        ('Ninja', 'Ninja')
    )

    name = models.CharField(max_length=6, choices=difficulties)


class Recipe(models.Model):
    difficulties = (
        ('noob', 'Noob'),
        ('master', 'Master'),
        ('ninja', 'Ninja')
    )
    title = models.CharField(max_length=40)
    difficulty = models.CharField(max_length=6, choices=difficulties)
    calories = models.IntegerField()
    cooking_time = models.IntegerField()


class RecipeIngredients(models.Model):
    ingredient = models.ForeignKey("ingredients.Ingredient", on_delete=models.CASCADE)
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE, null=True)
    required = models.BooleanField(default=False)
    grams = models.IntegerField()

    class Meta:
        db_table = "recipes_recipe__ingredients"
