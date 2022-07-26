from django import forms
from .models import UserAddress


class LoginUserForm(forms.Form):
    email = forms.CharField(label='E-Mail', required=True, error_messages={'required': 'Введите E-Mail!'})
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль', required=True,
                               error_messages={'required': 'Введите пароль!'})


class PasswordChangeForm(forms.Form):
    password_now = forms.CharField(label='Текущий пароль', widget=forms.PasswordInput, error_messages={'required': ''})
    password = forms.CharField(label='Новый пароль', widget=forms.PasswordInput, error_messages={'required': ''})
    password1 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput,
                                error_messages={'required': ''})


class AccountEditForm(forms.Form):
    first_name = forms.CharField(label='Имя', error_messages={'required': ''})
    second_name = forms.CharField(label='Фамилия', error_messages={'required': ''})
    birthday = forms.DateField(label='Дата рождения', error_messages={'required': ''})


class AddressesForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = ['country', 'city', 'zip_code', 'street', 'street_number', 'comment', 'phone', 'address_name']
