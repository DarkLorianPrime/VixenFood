from django.urls import path
from rest_framework.routers import SimpleRouter

from recipes import views

# , "post": "create"
router = SimpleRouter()
router.register(r'recipes', views.RecipesViewSet, basename="recipes")
urlpatterns = router.urls

