from django.urls import path
from .views import (
    tweet_delete_view,   
    tweet_detail_view,
    tweet_action_view,
    list_view, 
    feed_view,
    tweet_create
)

urlpatterns = [
    path('', list_view),
    path('feed/', feed_view),
    path('action/', tweet_action_view),
    path('create/', tweet_create),
    path('<int:tweet_id>/', tweet_detail_view),
    path('<int:tweet_id>/delete/', tweet_delete_view)
]
