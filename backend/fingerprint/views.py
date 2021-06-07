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
            fImage = cv2.imread("media/" + str(file))

            for i in range(len(data)):
                DbImage = cv2.imread(os.getcwd() + data[i].get('fingerprint').replace("http://127.0.0.1:8000",""))
                if(isMatch(fImage, DbImage)):
                    response_result.append(data[i])

            #The image came along with the request will be deleted after serving its purpose        
            try:
                default_storage.delete(str(file_name))
            except:
                print("The image could not be deleted")        

            return Response(response_result)    
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    