from django.shortcuts import render
from rest_framework.views import APIView

from . import serializers
# from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
#from django.http import HttpResponse
from rest_framework import status, permissions
from rest_framework.renderers import HTMLFormRenderer, JSONRenderer, BrowsableAPIRenderer
from django.http import Http404
from DiseasePrediction2.RFPrediction import predict

class DiseasePrediction(APIView):
    serializer_class = serializers.PredictionSerializer
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer, HTMLFormRenderer)


    def post(self, request, format=None):
        serializer = serializers.PredictionSerializer(data = request.data)   

        #print(request.data)
        d = request.data
        s1 = d.get("s1")
        s2 = d.get("s2")
        s3 = d.get("s3")
        s4 = d.get("s4")
        s5 = d.get("s5")
        
        d_list = predict(s1,s2,s3,s4,s5)

        if serializer.is_valid():
            serializer.save()
            return Response(d_list, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def get(self, request):
    #     queryset = models.RespiratoryRate.objects.all()
    #     serializer = serializers.RespiratoryRateSerializer(queryset, many=True)
    #     return Response(serializer.data)
