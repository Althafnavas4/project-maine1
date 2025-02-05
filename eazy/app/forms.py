from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordResetForm






# forms.py
from django import forms
from .models import Order, UserProfile

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'phone_number', 'email', 'address']  # Removed 'product', 'quantity', 'size'
    
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        user = kwargs.get('initial', {}).get('user', None)
        
        if user:
            try:
                profile = UserProfile.objects.get(user=user)
                self.fields['customer_name'].initial = profile.name
                self.fields['phone_number'].initial = profile.phone_number
                self.fields['address'].initial = profile.address
                self.fields['email'].initial = user.email  # Email from user model
            except UserProfile.DoesNotExist:
                pass


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))




class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))







        # forms.py

from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name','address', 'phone_number', 'date_of_birth', 'gender','name', ]










