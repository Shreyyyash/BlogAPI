from django.shortcuts import render,HttpResponse
from rest_framework.response import Response
from .serializers import UserSignupSerializer,LoginSerializer,PasswordChangeSerializer
from rest_framework.views import APIView
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


# Create your views here.

# @method_decorator(csrf_exempt, name='post')
class UserAPIView(APIView):
    def post(self,request,*args, **kwargs):
        data=request.data
        serializer=UserSignupSerializer(data=data)
        if serializer.is_valid():
            user=serializer.save()
            token=serializer.get_tokens_for_user(user)
            return Response({'message':"Account Created","token":token},status=status.HTTP_201_CREATED)
        else:
            return Response({"data":serializer.errors,'message':"Something went wrong"},status=status.HTTP_400_BAD_REQUEST)

# @method_decorator(csrf_exempt, name='post')
class LoginAPIView(APIView):   
    def post(self,request,*args, **kwargs):
        try:
            data=request.data
            serializer=LoginSerializer(data=data)
            if serializer.is_valid():
                token=serializer.get_tokens_for_user(serializer.validated_data)
                return Response({"message":"Logged in successfully.","token":token},status=status.HTTP_200_OK)
            else:
                return Response({"data":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            print(e)
            return Response({'message':"Something went wrong"},status=status.HTTP_400_BAD_REQUEST)

# @method_decorator(csrf_exempt, name='post')
class PasswordChangeAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = PasswordChangeSerializer(data=data,context={"request":request})
            
            if serializer.is_valid():
                user=request.user
                # we can use this user directly in validation method but we have passed through context above request
                serializer.save(user=user)
                return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)