from django.urls import path

from .views import UserLoginView, AccountProfile, UserChangePassword

app_name = 'account'

urlpatterns = [
    path('', AccountProfile.as_view(), name='user_profile'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('change-password/', UserChangePassword.as_view(), name='change_password'),

]
