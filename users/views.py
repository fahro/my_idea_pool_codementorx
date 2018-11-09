from rest_framework.views import APIView, Response,status
from .serializers import UserSerializer,MyTokenObtainPairSerializer,MyTokenRefreshSerializer,BlackListTokenSerializer
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from rest_framework.generics import DestroyAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated,AllowAny
import jwt
from my_idea_pool.settings import SECRET_KEY
from .models import User
from django.shortcuts import  get_object_or_404


class RetrieveUserAPIView(APIView):

    def get(self,request):
        access_token = request.META.get('HTTP_X_ACCESS_TOKEN')
        decoded = jwt.decode(access_token,SECRET_KEY)
        user = get_object_or_404(User,pk=decoded['id'])
        serilazer = UserSerializer(user)
        return Response(serilazer.data)

class CreateUserAPIView(APIView):
    permission_classes = (AllowAny,)


    def post(self, request):
        user = request.data
        serializer = UserSerializer(data=user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            tokens = MyTokenObtainPairSerializer(request.data).validate(request.data)
            return Response(tokens, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)

   

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def delete(self,request):
       
        serializer  = BlackListTokenSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            refresh_token= serializer.validated_data['refresh_token']
            refresh_token.blacklist()
            print(refresh_token)
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)


class MyTokenRefreshView(TokenRefreshView):
    serializer_class = MyTokenRefreshSerializer


