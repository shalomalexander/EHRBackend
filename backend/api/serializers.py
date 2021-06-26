from rest_framework import serializers
from appV1 import models
from api import models as m

# from allauth.account.adapter import get_adapter
# from rest_auth.registration.serializers import RegisterSerializer

# class CustomPerInfoSerializer(RegisterSerializer):
#     AadhaarNumber = serializers.CharField(max_length=12)
#     def get_cleaned_data(self):
#         data_dict = super().get_cleaned_data()
#         data_dict['AadhaarNumber'] = self.validated_data.get('AadhaarNumber', '')
#         return data_dict

class PersonalInfoSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = models.PersonalInfo
        fields = '__all__'

    def get_photo_url(self, obj):
        request = self.context.get('request')
        photo_url = obj.fingerprint.url
        profile_url = obj.profilePicture.url
        return request.build_absolute_uri(photo_url)      

class EmergencyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EmergencyInfo
        fields = '__all__'

class InsuranceInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InsuranceInfo
        fields = ("id", "insuranceProvider","policyNumber","policyName","validTill")

class PrescriptionInfoPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PrescriptionInfo
        fields = ('prescriberId','prescriptionDate','symptoms','medicines','notes','userId')

class PrescriptionInfoGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PrescriptionInfo
        fields = '__all__'        

class OrganizationInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrganizationInfo
        fields = '__all__'

class MedicalPractitionerInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MedicalPractitionerInfo
        fields = '__all__'   

class MedicalPractitionerOrgInfoSerializer(serializers.ModelSerializer):
    orgId = OrganizationInfoSerializer()
    class Meta:
        model = models.MedicalPractitionerInfo
        fields = '__all__'          

class BloodPressureSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BloodPressure
        fields = '__all__'        

class BodyTemperatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BodyTemperature
        fields = '__all__'  

class HeartRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HeartRate
        fields = '__all__'

class RespiratoryRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RespiratoryRate
        fields = '__all__'    

class PharmacyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PharmacyInfo
        fields = '__all__'

class AccessVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AccessVerification
        fields = '__all__' 
        # exclude = ('verify_otp',) 


class AccessVerificationAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AccessVerification
        fields = '__all__'           

class OTPAccessVerificationSerializer(serializers.Serializer):
    otp = serializers.CharField()
    pid = serializers.CharField()
    did = serializers.CharField()

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return m.OTP(**validated_data)

class AccessPrescriptionSerializer(serializers.Serializer):
    did = serializers.CharField()
    pid = serializers.CharField()

    def create(self, validated_data):
        return m.AccessPrescription(**validated_data)     

#Serializer for Lab Report
class LabReportInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LabReportInfo
        fields = '__all__'           

    def get_report_url(self, obj):
        request = self.context.get('request')
        report_url = obj.report.url
        return request.build_absolute_uri(report_url) 

class InsuranceAgentInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InsuranceAgentInfo
        fields = '__all__'

class EnrollInsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EnrollInsurance  
        fields = '__all__'

class PatientToAgentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PatientToAgentRequest 
        fields = '__all__'
