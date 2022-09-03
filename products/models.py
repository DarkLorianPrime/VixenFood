from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    # calorie = models.IntegerField() Not required yet
