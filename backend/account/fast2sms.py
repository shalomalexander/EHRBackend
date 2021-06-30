# import required module
import os
import requests
import json
import sys
sys.path.append("..\env\\")
from env.environment import Environment_Variable
# mention url

class SMS:
    def __init__(self):
        super().__init__()

    def sendOTP(self, otp, phone_number):   
        url = "https://www.fast2sms.com/dev/bulk" 
        # create a dictionary
        my_data = {
        # Your default Sender ID
        'sender_id': 'FSTSMS',
        # Put your message here!
        'message': 'This is your HealHub OTP: ' + str(otp) + '. ' + '\nKindly do not share this with anyone due to security reasons.',
        'language': 'english',
        'route': 'p',
        # You can send sms to multiple numbers
        # separated by comma.
        'numbers': str(phone_number)
        }

        auth = Environment_Variable()
        auth_key = auth.get_val("FAST2SMS")
        print(str(auth_key))
    
        # create a dictionary
        headers = {
        'authorization': str(auth_key),
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache"
        }
        # make a post request
        response = requests.request("POST",
        url,
        data = my_data,
        headers = headers)

        #load json data from source
        returned_msg = json.loads(response.text)

        # print the send message
        print(returned_msg['message'])




if __name__ == "__main__":
    obj = SMS()
    obj.sendOTP(123456, 9899129257)
