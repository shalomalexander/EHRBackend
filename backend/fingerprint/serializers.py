from rest_framework import serializers
from appV1.models import PersonalInfo
from django.contrib.sites.models import Site


class FingerprintRequestSerializer(serializers.Serializer):
    fingerprint = serializers.ImageField()
    gender = serializers.CharField()

class FingerprintResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalInfo
        fields = ("profilePicture", "user", "firstName", "middleName", "lastName", "dateOfBirth",
                  "mobileNumber", "alternateMobileNumber", "fingerprint")

    def get_photo_url(self, obj):
        request = self.context.get('request')
        profile_url = obj.profilePicture.url
        return request.build_absolute_uri(profile_url)         
       