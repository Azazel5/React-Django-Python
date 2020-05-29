import random 
from django.db import models
from django.conf import settings
from django.db.models import Q

User = settings.AUTH_USER_MODEL

# Quotes used cause the tweet model has not been defined yet before this
class TweetLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey("Tweet", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class TweetQuerySet(models.QuerySet):
    """ A custom queryset class, which is later used by a model manager. 
    --------------------------------------------------------------------
    Creates some functions which can be accessed through the get_queryset
    function in the manager. The values_list attribute returns tuples as a
    queryset. Several filters can be used using a format like Q | Q where Q
    is one filter.
    """

    def by_username(self, user):
        return self.filter(user__username__iexact=user)
        
    def feed(self, user):
        profiles_exists = user.following.exists()
        followed_user_id = []
        if profiles_exists:
            followed_user_id = user.following.values_list("user__id", flat=True)

        return self.filter(
            Q(user__id__in=followed_user_id) |
            Q(user=user)
        ).distinct().order_by('-timestamp')

class TweetManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return TweetQuerySet(self.model, using=self._db)
    def feed(self, user):
        return self.get_queryset().feed(user)

class Tweet(models.Model):
    parent = models.ForeignKey('self', null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tweets')
    likes = models.ManyToManyField(User, related_name='tweet_user', blank=True, through=TweetLike)
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    # Initializing your custom model manager
    objects = TweetManager()

    class Meta:
        ordering = ['-id']

    @property
    def is_retweet(self):
        return self.parent != None 
        
    def __str__(self):
        return self.content if self.content != None else 'NoneContent'