from django.urls import path
from rest_framework.routers import SimpleRouter

from recipes import views

# , "post": "create"
router = SimpleRouter()
router.register(r'recipes', views.Recipes, basename="recipes")
urlpatterns = router.urls
# urlpatterns = [
#     path("/", views.IngredientsViewSet.as_view({"get": "list"}))
# ]
