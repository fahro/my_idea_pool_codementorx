from django.urls import path
from .views import CreateUserAPIView,authenticate_user
 
urlpatterns = [
    path('users', CreateUserAPIView.as_view()),
    path('access-tokens',authenticate_user),
]