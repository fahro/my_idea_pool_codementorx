from django.urls import path
from .views import CreateUserAPIView,MyTokenObtainPairView,MyTokenRefreshView


urlpatterns = [
    path('users', CreateUserAPIView.as_view()),
    path('api/token', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', MyTokenRefreshView.as_view(), name='token_refresh'),
]