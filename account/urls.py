from django.urls import path

from .views import *

urlpatterns = [
    path('user/register/', user_register, name='register'),
    path('user/login/', user_login, name='login'),
    path('user/logout/', user_logout, name='logout'),
    path('user/forgot_password/', forgot_password, name='forgot_password'),
    path('user/<int:id>/verify/',verify_otp, name='verify_otp'),
    path('user/<int:id>/reset/',password_reset, name='change_password'),
]
