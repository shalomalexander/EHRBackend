# # Download the helper library from https://www.twilio.com/docs/python/install

# #   from_='+12064294280',

# # Your Account Sid and Auth Token from twilio.com/console
# # DANGER! This is insecure. See http://twil.io/secure
# def sendOTP(message_body,message_to):
#     account_sid = 'AC04d9ddbb4105da6ad405e12709488071'
#     auth_token = '2fed696c4a6d5e6b60114bc92658eb06'
#     client = Client(account_sid, auth_token)

#     message = client.messages.create(
#                                 body = str(message_body),
#                                 from_ = '+12568012849',
#                                 to = '+91' + str(message_to)
#                             )
#     print(message.sid)


# # function to generate OTP 
# def generateOTP() : 

# 	digits = "0123456789"
# 	OTP = "" 

# 	for i in range(6) : 
# 		OTP += digits[math.floor(random.random() * 10)] 

# 	return OTP 

# def verifyUser(mobileNumber):
#     otp = generateOTP()
#     sendOTP(otp,mobileNumber)
#     return otp
