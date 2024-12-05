from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'address', 'city', 'state', 'postal_code', 'country', 'phone_number', 'email']
        
    # Optionally, you can add custom validation, e.g., for postal code or phone number
