from django.urls import path,include
from . import views
urlpatterns = [
    path('getallblog/',view=views.get_allblog,name="getallblog"),
    path('login/',views.login_view,name="login"),
    path('signup/',views.signup_view,name="signup"),
    path('myprofile/',views.myprofile_view,name="myprofile"),
    path('check/',views.check_tokens,name=""),
    path('logout/', views.logout_view, name='logout'),
    path('create/', views.create_blog_post, name='create_blog_post'),
    path('delete_blog/', views.delete_blog_post, name='delete_blog_post'),
    path('update_blog/<str:blog_uid>/', views.update_blog_post, name='update_blog_post'),
    path('blog_deatil/<str:blog_uid>/', views.blog_deatil, name='blog_detail'),
    path('add_comment/<str:blog_uid>/', views.add_comment, name='add_comment'),
    path('delete_comment/<str:comment_uid>/', views.delete_comment, name='delete_comment'),
    path('change_password/', views.change_password_view, name='change_password'),
]