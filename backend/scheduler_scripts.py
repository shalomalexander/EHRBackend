import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()
from appV1.models import MedicalPractitionerInfo
from api import serializers

#def main():
    # f = open("demo.txt", "a+")
    # queryset = MedicalPractitionerInfo.objects.all()
    # f.write(str(queryset) + "\n")
    # for qs in queryset.iterator():
    #     f.write(str(qs.name) + "\n")
    # f.close()


if __name__=="__main__":
    #main()
    print("Executed")