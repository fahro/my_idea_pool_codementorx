from rest_framework import serializers
from .models import Idea
from users.models import User
from users.serializers import UserSerializer

user = UserSerializer()

class IdeaSerializerPost(serializers.ModelSerializer):

    user_id = serializers.PrimaryKeyRelatedField(queryset = User.objects.all(),source='user', write_only=True)
    class Meta:
        model = Idea 
        fields = ('ease','confidence','impact','content','user_id')
        extra_kwargs = {
            'user_id': {'write_only': True},
        }
class IdeaSerializerPut(serializers.ModelSerializer):

    class Meta:
        model = Idea 
        fields = ('ease','confidence','impact','content')


class IdeaSerializerGet(serializers.ModelSerializer):

   class Meta:
        model = Idea 
        fields = ('id','content','impact','ease','confidence','average_score','created_at')