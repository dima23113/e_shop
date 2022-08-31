from django import forms


class LoginUserForm(forms.Form):
    email = forms.CharField(label='E-Mail', required=True, error_messages={'required': 'Введите E-Mail!'})
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль', required=True,
                               error_messages={'required': 'Введите пароль!'})


class PasswordChangeForm(forms.Form):
    password_now = forms.CharField(label='Текущий пароль', widget=forms.PasswordInput, error_messages={'required': ''})
    password = forms.CharField(label='Новый пароль', widget=forms.PasswordInput, error_messages={'required': ''})
    password1 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput,
                                error_messages={'required': ''})
