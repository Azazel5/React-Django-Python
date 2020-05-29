from django.urls import path, include
from .views import StripeView, PaymentSuccessful

urlpatterns = [
    path('', StripeView.as_view(), name='stripe'),
    path('success/', PaymentSuccessful.as_view(), name='payment-succesful')
]