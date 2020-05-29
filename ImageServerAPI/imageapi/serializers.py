from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from .models import UserImages


class UserCreateSerializer(serializers.ModelSerializer):
# The user create serializer, which performs CRUD operations 
# ---------------------------------------------------------------------
# validate_username: makes username longer than 8, make_password hashes 
# the serialized password using django's default hasher. Make sure that 
# the password field is write-only for security purposes. 

    def validate_username(self, value):
        if len(value) < 8:
            raise serializers.ValidationError('Username must be longer than 7 letters.')
        return value 

    def validate_password(self, value):
        return make_password(value)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

class UserImagesSerializer(serializers.ModelSerializer):
# The user images serializer which nests the UserCreateSerializer 
# -------------------------------------------------------------------------
# UserCreateSerializer's fields are read-only, as it is only for 
# reference purposes. Overriden create method to make sure to get the 
# current request's user and pass it as the owner (as it is the foreign key) 

    image_id = serializers.IntegerField(source='id', read_only=True)
    owner = UserCreateSerializer(read_only=True)

    class Meta:
        model = UserImages
        fields = ['image_id', 'title', 'owner', 'image']
    
    def create(self, validated_data):
        owner = self.context['request'].user
        image, created = UserImages.objects.get_or_create(owner=owner, **validated_data)
        return image 
    
