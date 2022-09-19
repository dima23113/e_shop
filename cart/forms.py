from django import forms


class DeliveryForm(forms.Form):
    delivery = [('pvz', 'Пункт выдачи'), ('cureer', 'Курьером')]
    address = forms.ChoiceField(required=True, initial=False)
    delivery_type = forms.ChoiceField(choices=delivery, required=True, initial=False)
