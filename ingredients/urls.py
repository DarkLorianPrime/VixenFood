from django.urls import path
from rest_framework.routers import SimpleRouter

from ingredients import views
# , "post": "create"
router = SimpleRouter()
router.register(r'', views.IngredientsViewSet)
urlpatterns = router.urls
# urlpatterns = [
#     path("/", views.IngredientsViewSet.as_view({"get": "list"}))
# ]
