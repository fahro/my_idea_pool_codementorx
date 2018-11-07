from rest_framework import serializers
from.models import User
 
 
class UserSerializer(serializers.ModelSerializer):
 
    avatar_url = serializers.ReadOnlyField()
 
    class Meta(object):
        model = User
        fields = ( 'email', 'name', 'avatar_url', 'password')
        extra_kwargs = {'password': {'write_only': True}}