from .serializers import CommentSerializer
from comment.models import Comment
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from main.models import Blog
from rest_framework import status

class CommentAPIView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    
    def get(self,request,*args, **kwargs):
        try:
            data=request.data
            user=request.user
            # blog_uid = data.get('blog_uid', None)
            blog_uid = request.query_params.get("uid")
            if blog_uid:
                user_comments = Comment.objects.filter(blog_id=blog_uid, user=user).select_related('blog').order_by('-created_at')
                other_comments = Comment.objects.filter(blog_id=blog_uid).exclude(user=user).select_related('blog').order_by('-created_at')
                    
                comments = list(user_comments) + list(other_comments)
                serializer=CommentSerializer(comments,many=True)
                return Response(serializer.data)
            return Response({"meaage":"Provide blog id to get comments"})
            
        except Exception as e:
            return Response({"message":str(e)})
    
    def post(self,request,*args, **kwargs):
        try:
            data = request.data.copy()
            # print(data)
            # blog_uid = data.get('blog_uid', None)
            blog_uid = request.query_params.get("uid")
            data["user"]=request.user.id
            data["blog"]=blog_uid
            # print(data)
            if blog_uid:
                serializer=CommentSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data,status=status.HTTP_201_CREATED)
               
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message":"Provide valid blog uid"},status=status.HTTP_403_FORBIDDEN)
            
        except Exception as e:
            return Response({"message":str(e)})
    
    def patch(self,request,*args, **kwargs):
        try:
            data = request.data.copy()
            comment_uid=data.get("uid",None)
            comment=Comment.objects.get(uid=comment_uid)

            if comment.user != request.user:
                return Response({"message": "You do not have permission to edit this."},status=status.HTTP_403_FORBIDDEN)
            
            serializer=CommentSerializer(comment,data=data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"Comment updated successfully","data":serializer.data},status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({"message":str(e)})
    
    def delete(self,request,*args, **kwargs):
        try:
            data=request.data
            # comment_uid=data.get('uid',None)
            comment_uid=request.query_params.get('uid',None)
            comment=Comment.objects.get(uid=comment_uid)
            if comment.user != request.user and comment.blog.user != request.user:
                return Response({"message": "You do not have permission to edit this."},status=status.HTTP_403_FORBIDDEN)
            comment.delete()
            return Response({"message":"Comment deleted successfully"},status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"message":str(e)})