from typing import Type

from django.db.models import Model


class AbstractRepository:
    model: Type[Model]

    def get_all(self):
        return self.model.objects.all()
