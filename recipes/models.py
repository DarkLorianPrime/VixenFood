from django.db import models
from django.db.models import Index


class Recipe(models.Model):
    difficulties = (
        ('noob', 'Noob'),
        ('master', 'Master'),
        ('ninja', 'Ninja')
    )
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

    # class Meta:
    #     indexes = (
    #         Index(name="covering_index", fields=("recipe",), include=("recipe",)),
    #     )
