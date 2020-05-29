import stripe
from django.urls import reverse
from django.conf import settings 
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

class StripeView(TemplateView):
    template_name = 'striped/stripe.html'

    def __init__(self):
        stripe.api_key = settings.STRIPE_API_KEY 

    # This is the server side key that Stripe checks
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk_key'] = settings.STRIPE_PUSH_KEY
        return context
    
    # This is the client charge, which has the source argument with the client side Stripe token
    def post(self, request, *args, **kwargs):
        charge = stripe.Charge.create(
            amount=amount,
            currency='usd',
            description='A Django charge',
            source=request.POST['stripeToken']
        )
        return redirect('payment-succesful',)

class PaymentSuccessful(TemplateView):
    template_name = 'striped/success.html'