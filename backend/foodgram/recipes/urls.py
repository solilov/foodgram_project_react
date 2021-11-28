from django.urls import include, path

from recipes.views import TagViewSet

from rest_framework.routers import DefaultRouter


app_name = 'recipes'

router = DefaultRouter()
router.register('tags', TagViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
