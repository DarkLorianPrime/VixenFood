from rest_framework.routers import SimpleRouter

from apps.products import views

router = SimpleRouter()

router.register('', views.ProductsViewSet, basename="products")
urlpatterns = router.urls
