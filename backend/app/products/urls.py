from django.urls import path
from rest_framework.routers import SimpleRouter

from products import views
from recipes.views import RecipesSearcher

router = SimpleRouter()

router.register('', views.ProductsViewSet, basename="products")
urlpatterns = [
    path("results/", RecipesSearcher.as_view({"get": "list"}))

] + router.urls
