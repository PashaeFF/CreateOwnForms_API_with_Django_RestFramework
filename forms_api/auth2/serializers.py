from rest_framework import serializers
from auth2.models import User 


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, write_only=True)

    def create(self, validated_data):

        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user
    
    class Meta():
        model = User
        fields = ('id', 'username', 'email', 'password')


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, write_only=True)
    
    class Meta():
        model = User
        fields = ('email', 'password')


class UserSerializer(serializers.ModelSerializer):
    class Meta():
        model = User
        fields = ('id','email','username')