from django.urls import path
from .views import CreateUserAPIView,MyTokenObtainPairView,MyTokenRefreshView,RetrieveUserAPIView


urlpatterns = [
    path('users', CreateUserAPIView.as_view()),
    path('access-tokens', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('access-tokens/refresh', MyTokenRefreshView.as_view(), name='token_refresh'),
    path('me',RetrieveUserAPIView.as_view()),

]