from django import forms


class LoginUserForm(forms.Form):
    email = forms.CharField(label='E-Mail', required=True, error_messages={'required': 'Введите E-Mail!'})
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль', required=True,
                               error_messages={'required': 'Введите пароль!'})
