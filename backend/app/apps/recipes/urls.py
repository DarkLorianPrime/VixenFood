from django.urls import path
from rest_framework.routers import SimpleRouter

from apps.recipes import views
from apps.recipes.views import RecipesSearcher

router = SimpleRouter()
router.register(r'', views.RecipesViewSet, basename="recipes")
router.register(r'(?P<recipe_id>\d+)/stages', views.StagesViewSet, basename="stages")
router.register(r'(?P<recipe_id>\d+)/ingredients', views.IngredientsViewSet, basename="ingredients")
urlpatterns = [
                  path("results/", RecipesSearcher.as_view({"get": "list"}))
              ] + router.urls
