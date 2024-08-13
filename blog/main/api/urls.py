from django.urls import path,include
from . import views

urlpatterns = [
    path('blog/',views.BlogAPIView.as_view()),
    path('allblog/',views.AllBlogAPIView.as_view()),
]
