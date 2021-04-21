from django import forms

class OtpForm(forms.Form):
    your_otp = forms.CharField(label='Your OTP', max_length=6)