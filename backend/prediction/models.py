from django.db import models

# Create your models here.

class Symptoms(object):
    
    def __init__(self, **kwargs):
        for field in ('s1', 's2', 's3', 's4', 's5'):
            setattr(self, field, kwargs.get(field, None))

    