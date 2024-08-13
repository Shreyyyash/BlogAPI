from django.urls import path,include
from . import views

urlpatterns = [
    path('api/',views.CommentAPIView.as_view()),
]