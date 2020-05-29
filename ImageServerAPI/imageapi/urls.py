from rest_framework import routers
from django.urls import path, include 

from .views import UserAPI, ImagesAPI

router = routers.DefaultRouter()
router.register('users', UserAPI)
router.register('images', ImagesAPI)

urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]
