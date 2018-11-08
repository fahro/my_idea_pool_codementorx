from django.urls import path,include
from . import views

urlpatterns = [
    path('ideas',views.IdeaView.as_view()),
    path('ideas/<uuid:pk>',views.IdeaView.as_view()),
]