from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, OTPSerializer 
from .models import User
from django.shortcuts import redirect

from account.otp_form import OtpForm


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
        serializer.is_valid()
    
        user = serializer.save()
        return Response(
            {
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "token": AuthToken.objects.create(user)[1]
            }
        )

#Login API
class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        user = serializer.validated_data
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
        serializer = UserSerializer(queryset, many=True)    #Serializer for Get
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

        #verification
        is_verified = self.verify_otp(entered_otp, phone_number)

        if is_verified:
            print("verified")
            User.objects.filter(phone_number = phone_number).update(verified_field = True)
        else:
            print("unverified")
                
        return Response("This is OTP" + str(entered_otp))    

    def verify_otp(self, entered_otp, ph_number):
        queryset = User.objects.get(phone_number = ph_number)
        print("This is query: ",queryset.otp)
        stored_otp = queryset.otp
        if entered_otp == stored_otp:
            return True
        else:
            return False


#Algorithm-2
#1. Enter username, phone no, password in frontend
#2. OTP generated for the user and stored in the User model.
#3. Then send OTP to the phone number.
#4. User will be directed to OTP page.(username or phonenumber will go along with OTP)
#5. He will enter the OTP.
#6. OTP will be matched with the backend.
#7. User model will have a field called "verified".
#8. Verified == False: User will be deleted from DB after 10 min
# 9. else: User will be saved. 

#Requirements
#1. Modfiy User model for extra fields (OTP, verified)
#2. create a new Serializer, Views
#3. Create URL for OTP page 






    # def sendOTP(self,message_body,message_to):
    #     account_sid = 'AC04d9ddbb4105da6ad405e12709488071'
    #     auth_token = '120ffb054bfeb0e0f162673a246294a1'
    #     client = Client(account_sid, auth_token)

    #     message = client.messages.create(
    #                                 body = str(message_body),
    #                                 from_ = '+12568012849',
    #                                 to = '+91' + str(message_to)
    #                             )
    #     print(message.sid)           

    # # function to generate OTP 
    # def generateOTP(self) : 

    #     digits = "0123456789"
    #     OTP = "" 

    #     for i in range(6) : 
    #         OTP += digits[math.floor(random.random() * 10)] 

    #     return OTP 

    # def verifyUser(self,mobileNumber):
    #     otp = self.generateOTP()
    #     self.sendOTP(otp,mobileNumber)
    #     return otp
    


# class TwilioVerification():    
#     def get_otp(request):
#         # if this is a POST request we need to process the form data
#         if request.method == 'POST':
#             # create a form instance and populate it with data from the request:
#             form = OtpForm(request.POST)
#             # check whether it's valid:
#             if form.is_valid():
#                 enteredOTP = verifyUser()
#                 if form == enteredOTP:
#                     return True
#         return
