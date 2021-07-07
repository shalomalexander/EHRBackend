from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, OTPSerializer, ResendOTPSerializer
from .models import User
from django.shortcuts import redirect

from account.otp_form import OtpForm
from rest_framework.exceptions import APIException
from appV1 import models


#from twilio.rest import Client
#import math, random

# from django.http import HttpResponseRedirect
# from .forms import OtpForm

# from twilio.rest import Client
# import math, random

#from rest_framework.views import APIView
# Create your views here.

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        print(User.objects.filter(username=request.data["username"]))

        if(User.objects.filter(username=request.data["username"])):
            raise APIException("Username already exist.")

        if(User.objects.filter(email=request.data["email"])):
            raise APIException("This email id already exist.")

        if(User.objects.filter(phone_number=request.data["phone_number"])):
            raise APIException("This phone number already exist.")

        serializer.is_valid()

        user = serializer.save()
        return Response(
            {
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "token": AuthToken.objects.create(user)[1]
            }
        )

# Login API


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        user = serializer.validated_data
       
      
        if not user:
            return Response({"detail":"Incorrect Credentials"}, status=500)
        
        ra = models.RecentActivity.objects.create(activity="Welcome back, You just logged in", user_id=user.get_id())
        ra.save() 
        return Response(
            {
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "token": AuthToken.objects.create(user)[1]
            }
        )


class UserAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class UserList(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)  # Serializer for Get
        return Response(serializer.data)


class OTPView(generics.GenericAPIView):
    serializer_class = OTPSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()

        print(request.data["otp"])
        print(request.data["phone_number"])

        entered_otp = request.data["otp"]
        phone_number = request.data["phone_number"]

        # verification
        is_verified = self.verify_otp(entered_otp, phone_number)

        if is_verified:
            print("verified")
            User.objects.filter(phone_number=phone_number).update(
                verified_field=True)
        else:
            raise APIException("OTP doesn't match")

        return Response("Success")

    def verify_otp(self, entered_otp, ph_number):
        queryset = User.objects.get(phone_number=ph_number)
        print("This is query: ", queryset.otp)
        stored_otp = queryset.otp
        if entered_otp == stored_otp:
            return True
        else:
            return False

from account.fast2sms import SMS
import math, random
class ResendOTPView(generics.GenericAPIView):
    serializer_class = ResendOTPSerializer

    def post(self, request):
        data=request.data
      

        print(data["phone_number"])
        phone_number = request.data["phone_number"]
        sms = SMS()
        otp = self.generateOTP()
        sms.sendOTP(otp=otp, phone_number = phone_number)
        User.objects.filter(phone_number=phone_number).update(otp=otp)

        

        return Response("Success", status=200)

    def generateOTP(self):
        digits = "0123456789"
        OTP = ""
        for i in range(6):
            OTP += digits[math.floor(random.random() * 10)]

        return OTP

    def sendOTP(self, message_body, message_to):
        account_sid = 'AC04d9ddbb4105da6ad405e12709488071'
        auth_token = '2fed696c4a6d5e6b60114bc92658eb06'
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body=str(message_body),
            from_='+12568012849',
            to='+91' + str(message_to)
        )
        print(message.sid)
