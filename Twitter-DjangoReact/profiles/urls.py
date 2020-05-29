from django.urls import path, include 

from .views import profile_detail_view, profile_update_view

urlpatterns = [
    path('edit/', profile_update_view, name='edit'),
    path('<str:username>/', profile_detail_view),
]

