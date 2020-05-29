from django.contrib.auth.models import User
from rest_framework import authentication

class DevAuthentication(authentication.BaseAuthentication):
    """ A custom authentication class for debugging on the client (react) side. 
    """
    def authenticate(self, request):
        qs = User.objects.filter(id=2)
        user = qs.order_by("?").first()
        return (user, None)