from rest_framework.routers import SimpleRouter

from recipes import views

router = SimpleRouter()
router.register(r'recipes', views.RecipesViewSet, basename="recipes")
router.register(r'stages', views.StagesViewSet, basename="stages")
urlpatterns = router.urls

