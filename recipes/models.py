from django.db import models


difficulties = (
    ('noob', 'Noob'),
    ('master', 'Master'),
    ('ninja', 'Ninja')
)


class Recipe(models.Model):
    title = models.CharField(max_length=40)
    difficulty = models.CharField(max_length=6, choices=difficulties)
    # calories = models.IntegerField() Not required yet
    cooking_time = models.IntegerField()


class Ingredient(models.Model):
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE, null=True)
    required = models.BooleanField(default=False)
    grams = models.IntegerField(default=0)
    count = models.IntegerField(default=0)


class CookingStep(models.Model):
    name = models.CharField(max_length=120)
    text = models.TextField()
    step = models.IntegerField(default=0)
    recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE)
