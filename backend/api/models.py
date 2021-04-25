from django.db import models

# Create your models here.
class OTP(object):
    def __init__(self, **kwargs):
        for field in ('otp', 'did', 'pid'):
            setattr(self, field, kwargs.get(field, None))