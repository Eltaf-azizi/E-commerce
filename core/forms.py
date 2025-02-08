from django import forms


class checkoutForm(forms.Form):
    street_address = forms.CharField()
    apartment_address = forms.CharField(required=False)