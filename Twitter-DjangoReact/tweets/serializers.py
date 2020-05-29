from django.conf import settings 
from rest_framework import serializers

from .models import Tweet 
from profiles.serializers import PublicProfileSerializer

TWEET_ACTION_OPTIONS = settings.TWEET_ACTION_OPTIONS
class TweetActionSerializer(serializers.Serializer):
    """ Just like the get_{field_name} function, we also have access to 
    the validate_{field_name} function, which is purely for validating the
    data. 
    """
    
    id = serializers.IntegerField()
    action = serializers.CharField()
    content = serializers.CharField(allow_blank=True, required=False)

    def validate_action(self, value):
        value = value.lower().strip()
        if not value in TWEET_ACTION_OPTIONS:
            raise serializers.ValidationError('This is not a valid action,')
        else:
            return value

class TweetCreateSerializer(serializers.ModelSerializer):
    user = PublicProfileSerializer(read_only=True, source='user.profile')
    likes = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Tweet 
        fields = [
            'user', 'id', 'content', 'likes',
            'timestamp'
        ]
        
    def get_likes(self, obj):
        return obj.likes.count()

    def validate_content(self, value):
        if len(value) > settings.MAX_TWEET_LENGTH:
            raise forms.ValidationError('This tweet is too long!')
        return value
    

class TweetSerializer(serializers.ModelSerializer):
    user = PublicProfileSerializer(read_only=True, source='user.profile')
    likes = serializers.SerializerMethodField(read_only=True)
    parent = TweetCreateSerializer(read_only=True)

    class Meta:
        model = Tweet 
        fields = [
            'user', 'id', 'content', 'likes',
            'is_retweet', 'parent', 'timestamp'
        ]

        
    def get_likes(self, obj):
        return obj.likes.count()

