from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordResetForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))




class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))










from .models import Size

class SizeSelectionForm(forms.Form):
    size = forms.ChoiceField(choices=[], label="Select Size")

    def __init__(self, shoe, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically add size choices based on available sizes for the shoe
        available_sizes = shoe.sizes.all()
        self.fields['size'].choices = [(size.id, size.size) for size in available_sizes]



