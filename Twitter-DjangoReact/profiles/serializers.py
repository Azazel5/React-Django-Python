from rest_framework import serializers

from .models import Profile 

class PublicProfileSerializer(serializers.ModelSerializer):
    """ Serailizer for the profile section. Some unique things here:
    ----------------------------------------------------------------
    the get_{field_name} can be overriden to alter field before 
    serialization. Serializers have self.context, so you can pass
    the request as context if you have to access it here.
    """

    first_name = serializers.SerializerMethodField(read_only=True)
    last_name = serializers.SerializerMethodField(read_only=True)
    username = serializers.SerializerMethodField(read_only=True)
    follower_count = serializers.SerializerMethodField(read_only=True)
    following_count = serializers.SerializerMethodField(read_only=True)
    is_following = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile 
        fields = [
            'first_name', 'last_name', 'bio',
            'location', 'follower_count', 
            'following_count', 'username', 'is_following'
        ]

    def get_is_following(self, obj):
        is_following = False 
        context = self.context 
        request = context.get('request')
        if request:
            is_following = request.user in obj.followers.all()
        return is_following 
    
    def get_first_name(self, obj):
        return obj.user.first_name
    
    def get_last_name(self, obj):
        return obj.user.last_name
    
    def get_username(self, obj):
        return obj.user.username 
    
    def get_follower_count(self, obj):
        return obj.followers.count() 
    
    def get_following_count(self, obj):
        return obj.user.following.count() 