from apps.products.models import Product
from core.abstracts.repositories import AbstractRepository


class ProductRepository(AbstractRepository):
    def __init__(self):
        self.model = Product
