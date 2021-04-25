from rest_framework import serializers
from .models import User 
from django.contrib.auth import authenticate


# User Serializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_MP', 'is_pharma', 'verified_field', 'phone_number')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'is_MP', 'is_pharma', 'phone_number')
        extra_kwargs = {'password':{'write_only':True }}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['email'], 
        validated_data['username'], validated_data['password'], validated_data['is_MP'], validated_data['is_pharma'],
        validated_data['phone_number'])    
        return user 

# Login Serializer

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user  
        raise serializers.ValidationError("Incorrect Credentials")    

#Serializer for OTP
class OTPSerializer(serializers.ModelSerializer):
      class Meta:
        model = User
        fields = ('phone_number','otp')

