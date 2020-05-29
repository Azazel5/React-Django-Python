from django.db import models
from django.contrib.auth.models import User 
from django.db.models.signals import post_save

class FollowerRelation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    """ A standard profile model. An interesting thing here is how related_name is 
    ------------------------------------------------------------------------------
    used. It is related to the User, so the following field can be used to see the 
    User's following. Otherwisde the followers.set_ method would have to be called.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=255, null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    followers = models.ManyToManyField(User, related_name='following', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

# Using signals to detect if a profile has been created or not. 
def user_did_save(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

post_save.connect(user_did_save, sender=User)