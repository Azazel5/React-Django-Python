from django.http import Http404
from rest_framework import mixins
from rest_framework import viewsets
from django.shortcuts import render
from django.contrib.auth.models import User 
from django_filters.rest_framework import DjangoFilterBackend

from .models import UserImages
from .serializers import UserCreateSerializer, UserImagesSerializer


class UserAPI(mixins.CreateModelMixin,
              mixins.ListModelMixin,
              mixins.RetrieveModelMixin,
              viewsets.GenericViewSet):
    """
    API for performing CRUD operations on the users 
    """
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

class ImagesAPI(mixins.CreateModelMixin,
                mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                viewsets.GenericViewSet):
    """
    The image API viewset for adding images. It has a nested serializer for specifying the user adding the 
    images. It can also query images by user id: example - /api/v1/images/?userid={val}
    """
    queryset = UserImages.objects.all()
    serializer_class = UserImagesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['owner']




