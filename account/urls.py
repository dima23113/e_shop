from django.urls import path

from .views import UserLoginView, AccountProfile

app_name = 'account'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('account', AccountProfile.as_view(), name='user_profile')
]
