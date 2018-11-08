from rest_framework import serializers
from.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer,TokenRefreshSerializer
from django.utils.six import text_type
from rest_framework_simplejwt.tokens import RefreshToken
class UserSerializer(serializers.ModelSerializer):
 
    avatar_url = serializers.ReadOnlyField()
 
    class Meta(object):
        model = User
        fields = ( 'email', 'name', 'avatar_url', 'password')
        extra_kwargs = {'password': {'write_only': True}}


class BlackListTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
   
    def validate(self,attrs):
        print("HEY!")
        try:
            print("REFRESH:",attrs['refresh_token'])
            refresh_token = RefreshToken(attrs['refresh_token'])
            print("HELLLLOOOO!")
        except:
            raise serializers.ValidationError(
                ('Invalid or expired token'),
            )
        return {'refresh_token':refresh_token}
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):


    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        return token

    def validate(self, attrs):
        self.user = User.objects.filter(email=attrs['email'],password=attrs['password'])

        if not self.user:
            raise serializers.ValidationError(
                ('No active account found with the given credentials'),
            )

        refresh = self.get_token(self.user[0])
        print("REFRESH",refresh)
        data = {}

        data['jwt'] = text_type(refresh.access_token)
        data['refresh_token'] = text_type(refresh)

        return data


class MyTokenRefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
    def validate(self, attrs):
        try:
            refresh_token = RefreshToken(attrs['refresh_token'])
        except:
            raise serializers.ValidationError(
                ('Invalid or expired token'),
            )
      

        data = {'jwt': text_type(refresh_token.access_token)}


        #refresh_token.set_jti()
        #refresh_token.set_exp()
        #data['refresh_token'] = text_type(refresh_token)

        return data

