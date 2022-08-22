from django.db import models


class Difficult(models.Model):
    difficulties = (
        ('Noob', 'Noob'),
        ('Master', 'Master'),
        ('Ninja', 'Ninja')
    )

    name = models.CharField(max_length=6, choices=difficulties)


class Recipe(models.Model):
    title = models.CharField(max_length=40)
    difficulty = models.ForeignKey("Difficult", on_delete=models.CASCADE)
    calories = models.IntegerField()
    cooking_time = models.TimeField()
