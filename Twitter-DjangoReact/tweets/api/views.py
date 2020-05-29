import random
from ..models import Tweet
from ..forms import TweetForm 
from django.conf import settings

from rest_framework.authentication import SessionAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from ..serializers import (
    TweetSerializer, 
    TweetCreateSerializer,
    TweetActionSerializer
)
from rest_framework.response import Response 
from django.utils.http import is_safe_url
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse 


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_create(request, *args, **kwargs):
    serializer = TweetCreateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
       serializer.save(user=request.user)
       return Response(serializer.data, status=201)
    return Response({}, status=400)

def get_paginated_queryset_response(qs, request):
    """ A utility function to setup a default pagination 
    object. The serialized data is passed here. A smart way 
    to code if using function based views. 
    """

    paginator = PageNumberPagination()
    paginator.page_size = 20 
    paginated_qs = paginator.paginate_queryset(qs, request)
    serializer = TweetSerializer(paginated_qs, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    username = request.GET.get('username')
    if username:
        qs = qs.by_username(username)
    serializer = TweetSerializer(qs, many=True)
    return get_paginated_queryset_response(qs, request)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def feed_view(request, *args, **kwargs):
    user = request.user 
    qs = Tweet.objects.feed(user)
    return get_paginated_queryset_response(qs, request)

@api_view(['GET'])
def tweet_detail_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    
    obj = qs.first()
    serializer = TweetSerializer(obj)
    return Response(serializer.data, status=200)

@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)

    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({'message': 'You cannot delete this tweet'}, status=401)

    obj = qs.first()
    obj.delete()

    return Response({'message': 'Tweet deleted!'}, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_action_view(request, *args, **kwargs):
    """ An endpoint for handling user-based actions, such as
    liking, unliking, or retweeting. This is a very basic 
    set-up, as the rest is handled on the react.js side. 
    """

    serializer = TweetActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data 
        tweet_id = data.get('id')
        action = data.get('action')
        content = data.get('content')

    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()

    if action == 'like':
        obj.likes.add(request.user)
        serializer = TweetSerializer(obj)
        return Response(serializer.data, status=200)
    elif action == 'unlike':
        obj.likes.remove(request.user)
        serializer = TweetSerializer(obj)
        return Response(serializer.data, status=200)
    elif action == 'retweet':
        newTweet = Tweet.objects.create(user=request.user, parent=obj, content=content)
        serializer = TweetSerializer(newTweet)
        return Response(serializer.data, status=201)

    return Response({}, status=200)

def tweet_create_view_pure_django(request, *args, **kwargs):
    user = request.user 
    if not request.user.is_authenticated:
        user = None 
        if request.is_ajax():
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)
    form = TweetForm(request.POST or None)
    next_url = request.POST.get('next') or None 
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = user 
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201)
        if next_url != None and is_safe_url(next_url, settings.ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status=400)

    return render(request, 'components/form.html', context={'form': form})
