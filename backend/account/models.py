from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import math, random 
from account.fast2sms import SMS
# Create your models here.
class MyUserManager(BaseUserManager):

    def create_user(self, email, username, password = None, is_MP=False, is_pharma=False, is_insurance=False, phone_number=None):
        if not email:
            raise ValueError("User must have an email")

        if not username:
            raise ValueError("User must have a username")

        if not phone_number or phone_number==None:
            raise ValueError("User must have a phone number") 

        #Generation of OTP for the user with the specific phone number
        sms = SMS()
        otp = self.generateOTP()
        sms.sendOTP(otp=otp, phone_number = phone_number)
        # self.sendOTP(otp, phone_number)
    
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            is_MP = is_MP,
            is_pharma = is_pharma,
            is_insurance = is_insurance,
            phone_number=phone_number,
            otp=otp
        )                    

        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.model(
            email = email,
            username = username,
            password = password
        )    

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.verified_field = True
        user.set_password(password)
        user.save(using = self._db)
        return user

    def generateOTP(self) : 
        digits = "0123456789"
        OTP = "" 
        for i in range(6) : 
            OTP += digits[math.floor(random.random() * 10)] 

        return OTP

    def sendOTP(self, message_body, message_to):
        account_sid = 'AC04d9ddbb4105da6ad405e12709488071'
        auth_token = '2fed696c4a6d5e6b60114bc92658eb06'
        client = Client(account_sid, auth_token)

        message = client.messages.create(
                                    body = str(message_body),
                                    from_ = '+12568012849',
                                    to = '+91' + str(message_to)
                                )
        print(message.sid)
    

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True, max_length = 30)
    date_joined = models.DateTimeField(auto_now_add = True)
    last_joined = models.DateTimeField(auto_now_add = True)
    is_admin = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)
    is_MP = models.BooleanField(default = False)  #MP = Medical Practitioner
    is_pharma = models.BooleanField(default = False) # for pharmacy users
    is_insurance = models.BooleanField(default = False) # for Insurance Agents User
    phone_number = models.CharField(unique=True, max_length=10) # User's unique Phone Number
    
    otp = models.CharField(max_length=6, default="000000")
    verified_field = models.BooleanField(default = False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    objects = MyUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj = None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def get_phone_number(self):
        return self.phone_number