from django.shortcuts import render
from django.shortcuts import render,HttpResponse
from rest_framework.response import Response
from .serializers import BlogSerializer
from main.models import Blog
from rest_framework.views import APIView
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q
from main.api.paginaton import CustomBlogPAgination


# Create your views here.
class AllBlogAPIView(APIView):
    def get(self,request,*args, **kwargs):
        blog = Blog.objects.all().order_by('-created_at')

        blog_uid=request.query_params.get("uid",None)
        if blog_uid:
            try:
                blog = Blog.objects.get(uid=blog_uid)
                serializer = BlogSerializer(blog, context={'request': request})
                return Response(serializer.data)
            except Blog.DoesNotExist:
                return Response({"detail": "Blog post not found."}, status=status.HTTP_404_NOT_FOUND)

        search_query = request.query_params.get('search', '')
        if search_query:
            blog = blog.filter(
            Q(title__icontains=search_query) | Q(content__icontains=search_query)
            )            
        paginator=CustomBlogPAgination()
        blog=paginator.paginate_queryset(blog,request)
        serializer=BlogSerializer(blog,many=True,context={'request': request})
        return paginator.get_paginated_response(serializer.data)       
    

class BlogAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    
    def get(self,request,*args, **kwargs):
        user=request.user
        if user.is_authenticated:
            blog=Blog.objects.filter(user=user).select_related('user').order_by("-created_at")
            
            blog_uid=request.query_params.get("uid",None)
            if blog_uid:
                try:
                    blog = Blog.objects.get(uid=blog_uid)
                    serializer = BlogSerializer(blog, context={'request': request})
                    return Response(serializer.data)
                except Blog.DoesNotExist:
                    return Response({"detail": "Blog post not found."}, status=status.HTTP_404_NOT_FOUND)

            search_query = request.query_params.get('search', '')
            if search_query:
                blog = blog.filter(
                Q(title__icontains=search_query) | Q(content__icontains=search_query)
                )            
            
            serializer=BlogSerializer(blog,many=True,context={'request': request})
            return Response(serializer.data)
        # added this only for default browsable api
        else:
            return Response({"detail": "Authentication credentials were not provided."},status=status.HTTP_401_UNAUTHORIZED)
    
    def post(self,request,*args, **kwargs):      
        try:
            data = request.data.copy()
            data['user'] = request.user.id
            serializer=BlogSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"Blog posted successfully","data":serializer.data},status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"e":str(e)})
    
    def patch(self,request,*args, **kwargs):
        try:
            data=request.data.copy()
            # print(data)
            uid=data.get('uid')
            blog=Blog.objects.get(uid=uid)
            # print(blog)
            print()
            if request.user != blog.user:
                return Response({"message": "You do not have permission to edit this post."},status=status.HTTP_403_FORBIDDEN)
            
            serializer=BlogSerializer(blog,data=data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"Blog updated successfully","data":serializer.data},status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message":str(e)})
    
    def delete(self,request,*args, **kwargs):
        try:
            data=request.data.copy()
            uid=data.get('uid')
            blog=Blog.objects.get(uid=uid)
            if request.user != blog.user:
                return Response({"message": "You do not have permission to delete this post."},status=status.HTTP_403_FORBIDDEN)
            
            blog.delete()
            return Response({"message":"Blog deleted successfully"},status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"message":str(e)})