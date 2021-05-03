from rest_framework import serializers
from .models import Symptoms

class PredictionSerializer(serializers.Serializer):
    s1 = serializers.CharField()
    s2 = serializers.CharField()
    s3 = serializers.CharField()
    s4 = serializers.CharField(allow_blank=True, required=False)
    s5 = serializers.CharField(allow_blank=True, required=False)
    
    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Symptoms(**validated_data)