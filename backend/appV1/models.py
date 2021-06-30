from django.db import models
from django import forms
from django.contrib.postgres.fields import ArrayField
import datetime
from backend.settings import AUTH_USER_MODEL

# Create your models here.
class PersonalInfo(models.Model):
    user=models.OneToOneField(AUTH_USER_MODEL, on_delete = models.CASCADE)
    firstName = models.CharField(max_length=100)
    middleName = models.CharField(max_length=100,null=True, blank=True)
    lastName = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length = 10, null = True)
    dateOfBirth = models.DateField(max_length=10, null = True)
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('AB+', 'AB+'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB-', 'AB-'),
        ('O-', 'O-'),
        ('O+', 'O+'),
    ]
    bloodGroup = models.CharField(
        max_length=3,
        choices=BLOOD_GROUP_CHOICES,
        null=True
    )

    emailId = models.EmailField(max_length=50, null = True)
    mobileNumber = models.CharField(max_length=10, null = True)
    alternateMobileNumber = models.CharField(max_length=10, null = True, blank=True)
    addressLine = models.CharField(max_length=50, null = True)
    cityOrTown = models.CharField(max_length=20, null = True)
    district = models.CharField(max_length=20, null = True)
    state = models.CharField(max_length=20, null = True)
    pin = models.CharField(max_length=6, null = True)
    aadhaarCardNumber = models.CharField(max_length=14, null=True)
    fingerprint = models.ImageField(upload_to='fingerprints/', null = True)
    profilePicture = models.ImageField(upload_to='profile_pictures/', null = True)

class EmergencyInfo(models.Model):                                      
    relativeName = models.CharField(max_length=100)
    relationship = models.CharField(max_length=20)
    primaryContactNumber = models.CharField(max_length=10)
    secondaryContactNumber = models.CharField(max_length=10, null = True)
    relativeAddress = models.CharField(max_length=100)
    userId = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)

class InsuranceInfo(models.Model):
    insuranceProvider = models.CharField(max_length=50)
    policyNumber = models.CharField(max_length=20, unique=True)
    policyName = models.CharField(max_length=50)
    validTill = models.DateField()
    userId = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)    
    
class OrganizationInfo(models.Model):
    #organization must not be deleted
    orgName = models.CharField(max_length=20)
    address = models.CharField(max_length=30)
    ACTIVE_CHOICES = [
        ("Y","YES"),
        ("N", "NO")
    ]
    activeIndicator = models.CharField(max_length=1, choices=ACTIVE_CHOICES)
    orgRegNumber = models.CharField(max_length=26, unique=True)

class MedicalPractitionerInfo(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=30)
    licenseNumber = models.CharField(max_length=20)
    profile = models.CharField(max_length=20)
    mobileNumber = models.CharField(max_length=10)
    address = models.CharField(max_length=30)
    ACTIVE_CHOICES = [
        ("Y","YES"),
        ("N", "NO")
    ]
    activeIndicator = models.CharField(default="N", max_length=1, choices=ACTIVE_CHOICES)
    orgId = models.ForeignKey(OrganizationInfo, null= True, on_delete = models.SET_NULL)

class PharmacyInfo(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    pharmacyName = models.CharField(max_length = 20)
    address = models.CharField(max_length = 50)
    lat = models.CharField(max_length = 20)
    lon = models.CharField(max_length = 20)
    mobileNumber = models.CharField(max_length = 10)

class PrescriptionInfo(models.Model):
    ADDED_BY_CHOICES = [
        ('Self', 'User'),
        ('Doctor', 'Doctor'),
    ]
    addedBy = models.CharField(
        max_length=6,
        choices=ADDED_BY_CHOICES,
    )
    hospitalOrClinic = models.CharField(max_length=50, null = True) # fetched from MP table
    doctorName = models.CharField(max_length=20, null = True)  # fetched from MP Table
    prescriptionDate = models.DateField(default= datetime.date.today)  
    contactNumber = models.CharField(max_length=10, null=True) # fetched from MP table
    address = models.CharField(max_length=50, null=True) # fetched from MP table
    
    symptoms = models.TextField(max_length=255, null=True)
    medicines = models.TextField(max_length=255, null=True) #put this field comma seperated
    notes = models.CharField(max_length=255, null=True)
    prescriptionAttachment = models.ImageField(null = True)
    prescriberId = models.ForeignKey(AUTH_USER_MODEL, null = True, on_delete=models.SET_NULL, related_name='prescriberId')
    userId = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='userId')
    
    #Automatically filling fields when prescriber id is provided.
    def save(self, *args, **kwargs):
        if not self.id and self.prescriberId is not None:
            MP = MedicalPractitionerInfo.objects.get(user = self.prescriberId.__dict__['id'])
            org = OrganizationInfo.objects.get(id=MP.__dict__['orgId_id'])
            self.hospitalOrClinic = org.__dict__['orgName']
            self.address = org.__dict__['address']
            self.doctorName = MP.__dict__['name']
            self.contactNumber = MP.__dict__['mobileNumber']
        super(PrescriptionInfo, self).save()


class BloodPressure(models.Model):
    systolic = models.IntegerField()
    diastolic = models.IntegerField()
    date = models.DateField(default = datetime.date.today)
    notes = models.CharField(max_length=255, null = True)
    userId = models.ForeignKey(AUTH_USER_MODEL, on_delete = models.CASCADE)


class BodyTemperature(models.Model):
    temp = models.FloatField()
    date = models.DateField(default = datetime.date.today)
    notes = models.CharField(max_length=255, null = True)
    userId = models.ForeignKey(AUTH_USER_MODEL, on_delete = models.CASCADE)

class HeartRate(models.Model):
    rate = models.IntegerField()
    date = models.DateField(default = datetime.date.today)
    notes = models.CharField(max_length=255, null = True)
    userId = models.ForeignKey(AUTH_USER_MODEL, on_delete = models.CASCADE)

class RespiratoryRate(models.Model):
    rate = models.IntegerField()
    date = models.DateField(default = datetime.date.today)
    notes = models.CharField(max_length = 255, null = True)
    userId = models.ForeignKey(AUTH_USER_MODEL, on_delete = models.CASCADE)

class AccessVerification(models.Model):
    did = models.ForeignKey(AUTH_USER_MODEL, on_delete = models.CASCADE, related_name='did')
    pid =  models.ForeignKey(AUTH_USER_MODEL, on_delete = models.CASCADE, related_name='pid')
    otp = models.CharField(max_length=6, default="000000")
    verify_otp = models.BooleanField(default = False)
    prescription_field = models.BooleanField(default = False)
    blood_pressure_field = models.BooleanField(default = False)

    def get_otp(self):
        return self.otp

    def set_verify_otp(self,data):
        self.verify_otp = data 
     
    def get_verify_otp(self):
        return self.verify_otp 

    def get_prescription_field(self):
        return self.prescription_field    

#Creating Model for Lab Report
class LabReportInfo(models.Model):
    title = models.CharField(max_length=20, null = True)
    report = models.FileField(upload_to='labreports/', null = True)
    tag = models.CharField(max_length=20, null = True)
    report_status = models.CharField(max_length=20, null = True)
    created_on = models.DateField(default = datetime.date.today)  
    userId = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    
class InsuranceAgentInfo(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=30, null = True)
    licenseNumber = models.CharField(max_length=20, null = True)
    mobileNumber = models.CharField(max_length=10, null = True)
    description= models.TextField(max_length=255, null=True) 
    address = models.CharField(max_length=30, null = True)
    tags = models.TextField(max_length=255, null = True, blank=True)
    ACTIVE_CHOICES = [
        ("Y","YES"),
        ("N", "NO")
    ]
    activeIndicator = models.CharField(default="N", max_length=1, choices=ACTIVE_CHOICES)
    organization = models.CharField(max_length=30, null=True)

class EnrollInsurance(models.Model): 
    agentId =  models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="enroll_agent_id")   
    userId = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="enroll_user_id")
    created_on =  models.DateField(default = datetime.date.today)  
    validTill = models.DateField(null = True) 
    policyProvider =  models.CharField(max_length=30, null=True)
    policyName = models.CharField(max_length=30, null=True)
    policyNumber = models.CharField(max_length=30, null=True)  

class PatientToAgentRequest(models.Model):
    agentId =  models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="pta_agent_id")   
    userId = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="pta_user_id")  
    created_on =  models.DateField(default = datetime.date.today)  
    tags = models.CharField(max_length=255, null=True, blank=True)
    is_approved = models.BooleanField(default = False)
    is_declined = models.BooleanField(default = False)

