from django.contrib import admin

# Register your models here.
from appV1 import models

admin.site.register(models.PersonalInfo)
admin.site.register(models.EmergencyInfo)
admin.site.register(models.InsuranceInfo)
admin.site.register(models.PrescriptionInfo)
admin.site.register(models.OrganizationInfo)
admin.site.register(models.MedicalPractitionerInfo)
admin.site.register(models.BloodPressure)
admin.site.register(models.BodyTemperature)
admin.site.register(models.HeartRate)
admin.site.register(models.RespiratoryRate)
admin.site.register(models.PharmacyInfo)

