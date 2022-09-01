from django.urls import path

from .views import UserLoginView, AccountProfile, UserChangePassword, UserLogoutView, AccountEditView, \
    AccountAddressesView, AccountAddAddressView, AddressEditView

app_name = 'account'

urlpatterns = [
    path('', AccountProfile.as_view(), name='user_profile'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('change-password/', UserChangePassword.as_view(), name='change_password'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('account-edit/', AccountEditView.as_view(), name='account_edit'),
    path('account-address/edit/', AddressEditView.as_view(), name='edit_address'),
    path('account-addresess/add/', AccountAddAddressView.as_view(), name='add_address'),
    path('account-addresses/', AccountAddressesView.as_view(), name='account_addresses')
]
