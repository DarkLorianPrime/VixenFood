from rest_framework.routers import SimpleRouter

from apps.recipes import views

router = SimpleRouter()
router.register(r'', views.RecipesViewSet, basename="recipes")
router.register(r'(?P<recipe_id>\d+)/stages', views.StagesViewSet, basename="stages")
urlpatterns = router.urls

