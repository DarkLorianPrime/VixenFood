from typing import Self

from django.db import models


difficulties = (
    ('noob', 'Noob'),
    ('master', 'Master'),
    ('ninja', 'Ninja')
)


class Recipe(models.Model):
    title = models.CharField(max_length=40)
    difficulty = models.CharField(max_length=6, choices=difficulties)
    cooking_time = models.IntegerField()


class Ingredient(models.Model):
    product = models.ForeignKey("apps.products.Product", on_delete=models.CASCADE)
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE, null=True)
    required = models.BooleanField(default=False)
    grams = models.IntegerField(default=0)
    count = models.IntegerField(default=0)


class CookingStep(models.Model):
    step = models.IntegerField(default=1)
    name = models.CharField(max_length=120)
    text = models.TextField()
    recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE)

    def swap_step(self, other_model: Self):
        self.step, other_model.step = other_model.step, self.step
        self.save()
        other_model.save()

    def save(self, *args, **kwargs):
        if self.pk:
            return super().save(*args, **kwargs)

        step = CookingStep.objects.filter(recipe_id=self.recipe.id).order_by("-id").first()
        if step:
            self.step = step.step + 1

        return super().save(*args, **kwargs)

