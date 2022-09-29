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
    grams = models.IntegerField()
    count = models.IntegerField()
