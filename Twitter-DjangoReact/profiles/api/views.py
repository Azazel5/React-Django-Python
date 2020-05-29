import random

from django.conf import settings

from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response 
from django.utils.http import is_safe_url
from django.contrib.auth.models import User 
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse

from ..models import Profile 
from ..serializers import PublicProfileSerializer


@api_view(['GET', 'POST', 'PATCH'])
def profile_detail_api_view(request, username, *args, **kwargs):
    """ An API endpoint to view details of the user. Uses the related_name
    ----------------------------------------------------------------------
    attribute to get a list of followers/following for the is_following 
    field. This endpoint is also used to follow a given user.
    """
    
    qs = Profile.objects.filter(user__username=username)
    if not qs.exists():
        return Response({"detail": "User not found"}, status=404)
    profile_obj = qs.first()
    data = request.data or {}
   
    if request.method == 'POST':
        me = request.user 
        action = data.get('action')
        if profile_obj.user != me:
            if action == 'follow':
                profile_obj.followers.add(me)
            elif action == 'unfollow':
                profile_obj.followers.remove(me)
            else:
                pass 
    
    serializer = PublicProfileSerializer(instance=profile_obj, context={"request": request})
    return Response(serializer.data, status=200)