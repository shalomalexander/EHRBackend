from django.shortcuts import render
from rest_framework.views import APIView
from appV1 import models
from . import serializers
# from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
#from django.http import HttpResponse
from rest_framework import status, permissions
from rest_framework.renderers import HTMLFormRenderer, JSONRenderer, BrowsableAPIRenderer
from django.http import Http404

# Create your views here.

class PersonalInfoList(APIView):
    serializer_class = serializers.PersonalInfoSerializer
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer, HTMLFormRenderer)
    def get(self, request):
        queryset = models.PersonalInfo.objects.all()
        serializer = serializers.PersonalInfoSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = serializers.PersonalInfoSerializer(data = request.data)         
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PersonalInfoOfSpecificUser(APIView):
    serializer_class = serializers.PersonalInfoSerializer
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer, HTMLFormRenderer)
    def get_object(self, pk):
        try:
            return models.PersonalInfo.objects.get(pk = pk)
        except models.PersonalInfo.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        queryset = self.get_object(pk)
        serializer = serializers.PersonalInfoSerializer(queryset, many=False)
        return Response(serializer.data)            


class EmergencyInfoList(APIView):
    serializer_class = serializers.EmergencyInfoSerializer
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer, HTMLFormRenderer)
    def get(self, request):
        queryset = models.EmergencyInfo.objects.all()
        serializer = serializers.EmergencyInfoSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = serializers.EmergencyInfoSerializer(data = request.data)         
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmergencyInfoOfSpecificUser(APIView):
    def get_object(self, fk):
        try:
            return models.EmergencyInfo.objects.filter(userId = fk)
        except models.PrescriptionInfo.DoesNotExist:
            raise Http404

    def get(self, request, fk, format=None):
        queryset = self.get_object(fk)
        serializer = serializers.EmergencyInfoSerializer(queryset, many=True)
        return Response(serializer.data)            

class InsuranceInfoList(APIView):
    serializer_class = serializers.InsuranceInfoSerializer

    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get(self, request):
        queryset = models.InsuranceInfo.objects.filter(userId = request.user)
        serializer = serializers.InsuranceInfoSerializer(queryset, many=True)
        print(request.user)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = serializers.InsuranceInfoSerializer(data = request.data)         
        
        if serializer.is_valid():
            serializer.save(userId = request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   

    def get_object(self, pk, user):
        try:
            return models.InsuranceInfo.objects.filter(userId = user).get(pk=pk)
        except models.InsuranceInfo.DoesNotExist:
            raise Http404        

    def delete(self, request, pk, format=None):
        queryset = self.get_object(pk = pk, user=request.user)
        #serializer = serializers.InsuranceInfoSerializer(queryset, many=False)
        temp = queryset
        queryset.delete() 
        return Response("Delete Successful!" + str(temp));      

class PrescriptionInfoList(APIView):
    #serializer_class = [ serializers.PrescriptionInfoPostSerializer, serializers.PrescriptionInfoGetSerializer ]
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer, HTMLFormRenderer)
    permissions_classes = [
        permissions.IsAuthenticated
    ]


    #This GET request is for doctors
    def get(self, request):
        #queryset = models.PrescriptionInfo.objects.all()
        queryset = models.PrescriptionInfo.objects.filter(prescriberId = request.user)
        serializer = serializers.PrescriptionInfoGetSerializer(queryset, many=True)    #Serializer for Get
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = serializers.PrescriptionInfoPostSerializer(data = request.data)       #Serializer for Post    
        
        if serializer.is_valid():
            #Checking whether the prescriber is a valid Prescriber
            pid = serializer.validated_data.get("prescriberId")
            #print(pid.__dict__['id'])
            ln = models.MedicalPractitionerInfo.objects.get(user = pid.__dict__['id']).__dict__["licenseNumber"]
            #print(ln)
            if(ln[0:1] == 'D'):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response("You dont have the right to prescribe medicines.")    
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

class PrescriptionInfoOfSpecificUser(APIView):
    permissions_classes = [
        permissions.IsAuthenticated
    ]

    serializer_classes = serializers.PrescriptionInfoGetSerializer

    def get_object(self, fk):
        try:
            return models.PrescriptionInfo.objects.filter(userId = fk)
        except models.PrescriptionInfo.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        userPrescriptions = self.get_object(request.user)
        serializer = serializers.PrescriptionInfoGetSerializer(userPrescriptions, many=True)
        return Response(serializer.data)    

class OrganizationInfoList(APIView):
    serializer_class = serializers.OrganizationInfoSerializer
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer, HTMLFormRenderer)
    def get(self, request):
        queryset = models.OrganizationInfo.objects.all()
        serializer = serializers.OrganizationInfoSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = serializers.OrganizationInfoSerializer(data = request.data)         
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

class OrganizationInfoDetail(APIView):
    serializer_class = serializers.OrganizationInfoSerializer
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer, HTMLFormRenderer)
    def get_object(self, pk):
        try:
            return models.OrganizationInfo.objects.get(pk=pk)
        except models.OrganizationInfo.DoesNotExist:
            raise Http404 

    def get(self, request, pk, format=None):
        organization = self.get_object(pk)
        serializer = serializers.OrganizationInfoSerializer(organization)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        organization = self.get_object(pk)
        serializer = serializers.OrganizationInfoSerializer(organization, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                                        

class MedicalPractitionerInfoList(APIView):
    serializer_class = serializers.MedicalPractitionerInfoSerializer
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer, HTMLFormRenderer)
    permissions_classes = [
        permissions.IsAuthenticated
    ]

    def get(self, request):
        queryset = models.MedicalPractitionerInfo.objects.all()
        serializer = serializers.MedicalPractitionerInfoSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = serializers.MedicalPractitionerInfoSerializer(data = request.data)         
        
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   

    def get_object(self, pk, user):
        try:
            return models.MedicalPractitionerInfo.objects.filter(user = user).get(pk=pk)
        except models.MedicalPractitionerInfo.DoesNotExist:
            raise Http404    

    def delete(self, request, pk, format=None):
        queryset = self.get_object(pk = pk, user=request.user)
        #serializer = serializers.InsuranceInfoSerializer(queryset, many=False)
        queryset.delete() 
        return Response("Delete Successful!");                                 

class MedicalPractitionerInfoOfSpecificOrganization(APIView):
    def get_object(self, fk):
        try:
            return models.MedicalPractitionerInfo.objects.filter(orgId = fk, )
        except models.MedicalPractitionerInfo.DoesNotExist:
            raise Http404

    def get(self, request, fk, format=None):
        medicalPractitioner = self.get_object(fk)
        serializer = serializers.MedicalPractitionerInfoSerializer(medicalPractitioner, many=True)
        return Response(serializer.data)                


class PharmacyInfoList(APIView):
    serializer_class = serializers.PharmacyInfoSerializer
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer, HTMLFormRenderer)
    def get(self, request, format=None):
        queryset = models.PharmacyInfo.objects.all()
        serializer = serializers.PharmacyInfoSerializer(queryset, many=True)
        return Response(serializer.data)

    #To input pharamacy details of particular user
    def post(self, request, format=None):
        serializer = serializers.PharmacyInfoSerializer(data = request.data)         
        
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)       


class BloodPressureList(APIView):
    serializer_class = serializers.BloodPressureSerializer
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer, HTMLFormRenderer)
    def get(self, request):
        queryset = models.BloodPressure.objects.all()
        serializer = serializers.BloodPressureSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = serializers.BloodPressureSerializer(data = request.data)         
    
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)      

class BloodPressureDetail(APIView):
    def get_object(self, pk):
        try:
            return models.BloodPressure.objects.get(id = pk)
        except models.BloodPressure.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        queryset = self.get_object(pk)
        serializer = serializers.BloodPressureSerializer(queryset)
        return Response(serializer.data)          

    def delete(self, request, pk, format=None):
        queryset = self.get_object(pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)                  

class BloodPressureOfSpecificUser(APIView):
    def get_object(self, fk):
        try:
            return models.BloodPressure.objects.filter(userId = fk, )
        except models.BloodPressure.DoesNotExist:
            raise Http404

    def get(self, request, fk, format=None):
        queryset = self.get_object(fk)
        serializer = serializers.BloodPressureSerializer(queryset, many=True)
        return Response(serializer.data)           

class BodyTemperatureList(APIView):
    serializer_class = serializers.BodyTemperatureSerializer
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer, HTMLFormRenderer)
    def get(self, request):
        queryset = models.BodyTemperature.objects.all()
        serializer = serializers.BodyTemperatureSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = serializers.BodyTemperatureSerializer(data = request.data)         
    
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)          

class BodyTemperatureDetail(APIView):
    def get_object(self, pk):
        try:
            return models.BodyTemperature.objects.get(id = pk)
        except models.BodyTemperature.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        queryset = self.get_object(pk)
        serializer = serializers.BodyTemperatureSerializer(queryset)
        return Response(serializer.data)          

    def delete(self, request, pk, format=None):
        queryset = self.get_object(pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class BodyTemperatureOfSpecificUser(APIView):
    def get_object(self, fk):
        try:
            return models.BodyTemperature.objects.filter(userId = fk, )
        except models.BodyTemperature.DoesNotExist:
            raise Http404

    def get(self, request, fk, format=None):
        queryset = self.get_object(fk)
        serializer = serializers.BodyTemperatureSerializer(queryset, many=True)
        return Response(serializer.data)


class HeartRateList(APIView):
    serializer_class = serializers.HeartRateSerializer
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer, HTMLFormRenderer)
    def get(self, request):
        queryset = models.HeartRate.objects.all()
        serializer = serializers.HeartRateSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = serializers.HeartRateSerializer(data = request.data)         
    
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)          

class HeartRateDetail(APIView):
    def get_object(self, pk):
        try:
            return models.HeartRate.objects.get(id = pk)
        except models.HeartRate.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        queryset = self.get_object(pk)
        serializer = serializers.HeartRateSerializer(queryset)
        return Response(serializer.data)          

    def delete(self, request, pk, format=None):
        queryset = self.get_object(pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class HeartRateOfSpecificUser(APIView):
    def get_object(self, fk):
        try:
            return models.HeartRate.objects.filter(userId = fk, )
        except models.HeartRate.DoesNotExist:
            raise Http404

    def get(self, request, fk, format=None):
        queryset = self.get_object(fk)
        serializer = serializers.HeartRateSerializer(queryset, many=True)
        return Response(serializer.data)  

##############################################################

class RespiratoryRateList(APIView):
    serializer_class = serializers.RespiratoryRateSerializer
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer, HTMLFormRenderer)
    def get(self, request):
        queryset = models.RespiratoryRate.objects.all()
        serializer = serializers.RespiratoryRateSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = serializers.RespiratoryRateSerializer(data = request.data)         
    
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)          

class RespiratoryRateDetail(APIView):
    def get_object(self, pk):
        try:
            return models.RespiratoryRate.objects.get(id = pk)
        except models.RespiratoryRate.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        queryset = self.get_object(pk)
        serializer = serializers.RespiratoryRateSerializer(queryset)
        return Response(serializer.data)          

    def delete(self, request, pk, format=None):
        queryset = self.get_object(pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class RespiratoryRateOfSpecificUser(APIView):
    def get_object(self, fk):
        try:
            return models.RespiratoryRate.objects.filter(userId = fk, )
        except models.RespiratoryRate.DoesNotExist:
            raise Http404

    def get(self, request, fk, format=None):
        queryset = self.get_object(fk)
        serializer = serializers.RespiratoryRateSerializer(queryset, many=True)
        return Response(serializer.data)          
