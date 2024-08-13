from django.urls import path,include
from . import views

urlpatterns = [
    path('signup/',views.UserAPIView.as_view()),
    path('login/',views.LoginAPIView.as_view()),
    path('change-password/',views.PasswordChangeAPIView.as_view()),
]
