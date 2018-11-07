from rest_framework.views import APIView, Response,status
from .serializers import UserSerializer,MyTokenObtainPairSerializer,MyTokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

class CreateUserAPIView(APIView):
    

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



class MyTokenRefreshView(TokenRefreshView):
    serializer_class = MyTokenRefreshSerializer