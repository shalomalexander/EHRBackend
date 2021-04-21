from django.urls import path, include
from .views import RegisterAPI, LoginAPI, UserAPI, UserList, OTPView
from knox import views as knox_views

urlpatterns = [
    path('api/auth', include('knox.urls')),
    path('api/auth/register', RegisterAPI.as_view()),
    path('api/auth/login', LoginAPI.as_view()),
    path('api/auth/user', UserAPI.as_view()),
    path('api/auth/logout', knox_views.LogoutView.as_view(), name="know_logout"),
    path('api/auth/userlist', UserList.as_view()),
    path('api/auth/verify_otp', OTPView.as_view())
]