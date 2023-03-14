from rest_framework import status, exceptions
from rest_framework.generics import GenericAPIView
from rest_framework.decorators import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from drf_yasg.utils import swagger_auto_schema
from .models import User
from django.conf import settings
from django.contrib.auth import authenticate
import jwt
from datetime import datetime, timedelta



class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterSerializer

    @swagger_auto_schema(operation_id="Registration", tags=['Authentication'], request_body=RegisterSerializer)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    @swagger_auto_schema(operation_id="Login", tags=['Authentication'], request_body=LoginSerializer)
    def post(self, request):
        email =  request.data.get('email', None)
        password = request.data.get('password', None)
        
        user = User.objects.filter(email=email).first()
        
        if user is None:
            raise exceptions.AuthenticationFailed("User not found")
        # if not user.check_password(password):
        #     raise exceptions.AuthenticationFailed("Incorrect password")
        if user:
            if password == user.password:
                payload = {
                    'id':user.id,
                    'username':user.username,
                    'email':user.email,
                    'exp':datetime.utcnow()+timedelta(hours=24)
                }
                token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
                response = Response()
                response.set_cookie(key='jwt',value=token, httponly=True)
                response.data = {
                    'jwt':token
                }
                return response
            return Response({'message':'Incorrect password'}, status=status.HTTP_400_BAD_REQUEST)
        

class UserView(GenericAPIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise exceptions.AuthenticationFailed("Unauthenticated...")
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Unauthenticated...")
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
class LogoutView(GenericAPIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message':'Logged out'
        }
        return response
