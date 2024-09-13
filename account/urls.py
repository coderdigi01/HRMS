from django.urls import path
from .views import *


urlpatterns = [
    # path('login/', loginView, name='login'),
    path('signup/', user_signup, name='signup'),
    path('send/otp/', send_otp, name='send_otp'),
    path('validate/otp/', validate_otp, name='validate_otp'),
    path('login/', user_login, name='login'),
    path('forgot-password/', forgot_password, name='forgot-password'),
    path('logout/', user_logout, name='logout'),
]

