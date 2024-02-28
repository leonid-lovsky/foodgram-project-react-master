from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from api.views import (
    UserViewSet, IngredientViewSet, RecipeViewSet, TagViewSet
)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'tags', TagViewSet)
router.register(r'recipes', RecipeViewSet)
router.register(r'ingredients', IngredientViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/', include('djoser.urls.authtoken')),
    # path('api/auth/session/', include('rest_framework.urls'))
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
