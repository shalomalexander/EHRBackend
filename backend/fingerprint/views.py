from django.shortcuts import render
from rest_framework.renderers import HTMLFormRenderer, JSONRenderer, BrowsableAPIRenderer
from . import serializers
from appV1.models import PersonalInfo
from django.core.files.storage import default_storage
import cv2
from rest_framework.views import APIView
from rest_framework.response import Response
import os
from .matcher import isMatch
from rest_framework import status
from appV1.models import RecentActivity

# Create your views here.
class MatchView(APIView):
    serializer_class = serializers.FingerprintRequestSerializer
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer, HTMLFormRenderer)

    def get(self, request, format=None):
        queryset = PersonalInfo.objects.all()
        serializer = serializers.FingerprintResponseSerializer(queryset, context={"request":request}, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = serializers.FingerprintRequestSerializer(data=request.data)
        print(request.data["did"])

        ra = RecentActivity.objects.create(activity="You have used the Fingerprint Access Tool", user_id=request.data["did"])
        ra.save()

        if serializer.is_valid():
            queryset = PersonalInfo.objects.filter(gender=request.data.get("gender"))
            response_serializer = serializers.FingerprintResponseSerializer(data=queryset, context={"request":request}, many=True)
            response_serializer.is_valid()
            data = response_serializer.data   
            response_result = []

            #Fetching the fingerprint from the request
            file = request.FILES['fingerprint']
            file_name = default_storage.save(file.name, file)

            #Fetching the saved fingerprint which came along with request
            if(os.getcwd() == "/home/shalomalexander"):
                fImage = cv2.imread("../../var/www/sites/mysite/backend/media/" + str(file)) # Will be executed for deployed version
            else:
                fImage = cv2.imread("media/" + str(file)) # Will be executed for local version

            for i in range(len(data)):
                if(os.getcwd() == "/home/shalomalexander"):
                    DbImage = cv2.imread("../../var/www/sites/mysite/backend" + data[i].get('fingerprint').replace("https://shalomalexander.pythonanywhere.com","")) # Will be executed for deployed version
                else:
                    DbImage = cv2.imread(os.getcwd() + data[i].get('fingerprint').replace("http://127.0.0.1:8000",""))  # Will be executed for local version

                if(isMatch(fImage, DbImage)):
                    response_result.append(data[i])

            #The image came along with the request will be deleted after serving its purpose        
            try:
                default_storage.delete(str(file_name))
            except:
                print("The image could not be deleted")  

            # print(response_result[0]["user"])   

            ra = RecentActivity.objects.create(activity="Your information was retrieved through Fingerprint by Doctor ID: "+str(request.data["did"]), user_id=response_result[0]["user"])
            ra.save()       

            return Response(response_result)    
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    