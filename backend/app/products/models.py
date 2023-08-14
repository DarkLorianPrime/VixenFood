from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.id)
