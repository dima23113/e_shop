from django import forms


class DeliveryForm(forms.Form):
    delivery = [('pvz', 'Пункт выдачи'), ('cureer', 'Курьером')]
    city = forms.CharField(required=True, initial=False, )
    zipcode = forms.CharField(required=True, initial=False)
    delivery_type = forms.ChoiceField(choices=delivery, required=True, initial=False)
